"""

@author  Thomas Mac Millan
         Cristobal Gonzalez
@version 1, 04/08/17
@abstract A partir de tenores y tasas publicadas por un broker, calculamos
          tasas cero cupón.

"""
from datetime import date
from dateutil.relativedelta import relativedelta
import various_functions_Mac as vf
import numpy as np
import pandas as pd
from scipy.optimize import newton
#import matplotlib.pyplot as plt
# Size of pandas window
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def main():
    # INICIO PARAMETROS INICIALES
    fecha = date(2017, 7, 19) #Fecha Inicial de INTERCAMBIO DE FLUJOS
    periodicidad = '6M'
    tenors, tasas = vf.importar_csv("./data.csv") #Importar Datos de CSV
    """ Importar Datos a mano
    tenors = ['3M','6M','9M','1Y','18M','2Y','3Y','4Y','5Y','6Y','7Y','8Y','9Y','10Y','12Y','15Y','20Y'] # Listado Tenores
    tasas = [2.4552,2.4202,2.3902,2.3902,2.4652,2.6402,2.8902,3.1302,3.3902,3.5702,3.7902,3.9602,4.0702,4.1502,4.2052,4.2552,4.4552]
    """
    # FIN PARAMETROS INICIALES

    num_col = 7 #numero de columnas para la matriz de datos
    size = (len(tenors),num_col) #Tamaño Matrix Tasas definido por usuario
    matrix = np.zeros(size, dtype=object) # Initialize Matrix


    # COLUMNA 1
    # Para la primera columna de la matrix, creo una variable auxiliar de 1 a 17
    for i in range(1,len(tenors)+1):
        matrix[i-1,0] = i
    # COLUMNA 2: Tenor en Meses
    # Para cada elemento de tenors, obtengo meses implicitos y lo guardo en implicit_tenor (numpy)
    implicit_tenor = np.empty([len(tenors)]) #Crea array numpy de largo numero de tenores
    for i in range(0,len(tenors)):
        implicit_tenor[i] = vf.ten(tenors[i])
    matrix[:,1] = implicit_tenor
    # COLUMNA 3: Incluyo Tasas
    matrix[:,2] = np.multiply(tasas,1/100)
    # COLUMNA 4 END DATE
    for i in range(0,len(tenors)):
        matrix[i,3] = vf.buss_day(vf.add_months(fecha,np.int(matrix[i,1])))
    # COLUMNA 5 DAYS FROM START
    for i in range(0,len(tenors)):
        matrix[i,4] = (matrix[i,3]-fecha).days
    # COLUMNA 7 DF
    matrix[:,6] = (1/(1+matrix[:,2]*matrix[:,4]/360))
    # COLUMNA 6 RATE START
    matrix[:,5] = (1/matrix[:,6]**(365/matrix[:,4])-1)*100

    #Matrix DF
    num_cupones = int((1/vf.ten(periodicidad))*vf.ten(tenors[-1]))
    size_matrix_df = (num_cupones,7)
    matrix_df = np.zeros(size_matrix_df, dtype=object)
    #Num Coupon
    matrix_df[:,0]=np.arange(6,int(vf.ten(tenors[-1]))+6,6)
    #End Date
    for i in range(0,num_cupones):
        matrix_df[i,2] = vf.buss_day(vf.add_months(fecha,matrix_df[i,0]))
    #Start Date
    matrix_df[:,1] = np.append(fecha,matrix_df[0:39,2])
    #Coupon Days
    for i in range(0,num_cupones):
        matrix_df[i,3] = (matrix_df[i,2]-matrix_df[i,1]).days
    #Days to End
    for i in range(0,num_cupones):
        matrix_df[i,4] = (matrix_df[i,2]-fecha).days
    #DF Es el INTERPOLADO
    curva_interp = vf.curva(matrix[:,4],matrix[:,6]) #Creo función de Curva
    for i in range(0,num_cupones):
        matrix_df[i,6] = curva_interp(matrix_df[i,4])
    #Rate
    matrix_df[:,5] = ((1/matrix_df[:,6])**(365/matrix_df[:,4])-1)*100


    #Matriz Tasas Interes
    aux_index = tenors.index("18M")
    col_matrix_int = len(tenors)-aux_index
    size_matrix_int = (len(matrix_df[:,0]),col_matrix_int-1)
    matrix_int = np.zeros(size_matrix_int)
    # Array Meses desde 2Y a 20Y para calcular IF es el último coupon
    array_meses_aux = matrix_df[:,0]
    array_meses_cupones_aux = matrix[aux_index+1:len(tenors),1]
    #For each year get i
    for j in range(0,len(array_meses_cupones_aux)): #Recorro Columnas
        for i in range(0,len(matrix_int[:,0])): #Recorro Filas
            if array_meses_aux[i] < array_meses_cupones_aux[j]:
                matrix_int[i,j] = (matrix[j+5,2]*matrix_df[i,3]/360 + 0)*100
            elif (array_meses_aux[i] == array_meses_cupones_aux[j]):
                matrix_int[i,j] = (matrix[j+5,2]*matrix_df[i,3]/360 + 1)*100
            else:
                matrix_int[i,j] = 0


    # Muestro la matrix con PANDAS
    names = ['Aux','Tenor en Meses','Mid TasaFija','End Date','Days Start','Rate Start','Df'] #Columnas
    data_inicial = pd.DataFrame(matrix, index=tenors, columns=names) #index es filas, columns columnas
    print()
    print('Datos Iniciales----------')
    print(data_inicial)
    # Muestro la matrix_df con PANDAS
    names_df = ['Num Coupon', 'Start Date', 'End Date', 'Coupon Days', 'Days to End', 'Rate', 'Df']
    data_df = pd.DataFrame(matrix_df, index=list(range(1, num_cupones+1)),columns=names_df)
    print()
    print('Matriz DF---------')
    print(data_df)
    # Muestro la matrix_int con PANDAS
    names_int = tenors[aux_index+1:len(tenors)]
    index_int = array_meses_aux
    data_int = pd.DataFrame(matrix_int, index=index_int, columns=names_int)
    print()
    print('Matriz Tasas--------')
    print(data_int)

# MINIMIZAR FACTORES-----------------------------------------
    # MINIMIZAR FACTORES DF
    def matrix_agrupada(matrix,matrix_df,matrix_int,num_cupones,j):
        def minimizador(df):
            matrix[j+5,6] = df
            curva_interp = vf.curva(matrix[:,4],matrix[:,6]) #Creo función de Curva
            #Matrix_df Columna Factores (Recalculo)
            for i in range(0,num_cupones):
                matrix_df[i,6] = curva_interp(matrix_df[i,4])
            error_2y = 100-np.sum(matrix_df[:,6]*(matrix_int[:,j]))
            return error_2y
        return minimizador
    #Minimizamos para cada Tenor
    for j in range (0,12):
        f_min = matrix_agrupada(matrix,matrix_df,matrix_int,num_cupones,j)
        df_min = newton(f_min, 0.5)

# MATRIZ FACTORES-----------------------------------------
    print()
    print('MATRIZ OPTIMIZADA---------')
    print(data_inicial)

    #Matriz Final
    matriz_final_filas = len(tenors)+2
    matrix_final = np.zeros((matriz_final_filas,3))
    #DF primeros días
    first_day = vf.buss_day(fecha + relativedelta(days=-2))
    second_day = vf.buss_day(fecha + relativedelta(days=-1))
    tasas_primeros_dias = 2.5/100
    matrix_final[0,0] = (fecha-second_day).days
    matrix_final[1,0] = (fecha-first_day).days
    matrix_final[0,2] = 1/(1+tasas_primeros_dias*(matrix_final[0,0]/360))
    matrix_final[1,2] = 1/(1+tasas_primeros_dias*(matrix_final[1,0]/360))
    for i in range(0,17):
        matrix_final[i+2:19,0] = (matrix[i,3]-first_day).days
    matrix_final[2:19,2] = matrix[:,6]*matrix_final[1,2]
    matrix_final[:,1] = (((1/matrix_final[:,2])**(365/matrix_final[:,0]))-1)*100
    matrix_final[:,2] = matrix_final[:,2]*100

    #Print Matrix Final
    print()
    print('Zero Coupon Rates-----------')
    names_final = ['Days', 'Tasa', 'Df']
    index_final = list(range(1,20))
    data_final = pd.DataFrame(matrix_final, index=index_final, columns=names_final)
    print(data_final)

    #Print Graph
    """
    plt.plot(matrix_final[:,0], matrix_final[:,1])
    plt.ylabel('Zero Coupon Rate')
    plt.xlabel('Days')
    plt.show()
    """

    #Export CSV
    data_final.to_csv('zero_coupon_curve.csv', header=False, index=False)

if __name__ == "__main__":
    main()
