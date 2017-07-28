# from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from scipy.interpolate import interp1d
import math
import csv

def ten(tenor):
    """
    Retorna el numero de meses implicito en un simbolo de tenor
    @param tenor (12M, 12m, 2Y, 3y, 2M) con otro tipo de string retorna cero.
    Lanzara un error si el argumento no es un string
    """
    symbol = tenor[-1:].lower() # pone en minusculas la Y o la M
    if symbol == "m":
        result = int(tenor[:-1])
    elif symbol == "y":
        result = 12 * int(tenor[:-1])
    else:
        result = 0
    return result


def buss_day(fecha, sentido="FOLLOW"):
    """
    Retorna el dia habil siguiente o anterior a una fecha si esta es sabado o domingo.

    @param (datetime.date) fecha
    @param (string) sentido

    Si fecha es un dia de lunes a viernes retorna la misma fecha, si fecha es un sabado o un domingo retorna
    el lunes siguiente si sentido = "FOLLOW" y retorna el viernes anterior si sentido = "PREVIOUS".
    Si sentido no es igual a "FOLLOW" o "PREVIOUS" entonces lo asumira como "FOLLOW".
    El valor por default de sentido es "FOLLOW".
    """
    dia_semana = fecha.isoweekday()  # Lunes = 1, ..., domingo = 7
    if sentido.lower() == "follow":
        if dia_semana == 6:  # dia sabado
            dias = timedelta(days=2)  # vamos a sumar 2 dias
        elif dia_semana == 7:
            dias = timedelta(days=1)  # vamos a sumar un dia
        else:
            dias = timedelta(days=0)  # no sumamos nada
    elif sentido.lower() == "previous":
        if dia_semana == 6:  # dia sabado
            dias = timedelta(days=-1)  # vamos a restar 1 dias
        elif dia_semana == 7:
            dias = timedelta(days=-2)  # vamos a restar 2 dias
        else:
            dias = timedelta(days=0)  # no restamos nada
    else:  # lo tratamos como si fuera "follow"
        if dia_semana == 6:  # dia sabado
            dias = timedelta(days=2)  # vamos a sumar 2 dias
        elif dia_semana == 7:
            dias = timedelta(days=1)  # vamos a sumar un dia
        else:
            dias = timedelta(days=0)  # no sumamos nada
    return fecha + dias


def add_months(fecha, num_meses):
    meses = relativedelta(months=num_meses)
    result = fecha + meses
    return result


def fechas_swap(fecha_inicial, periodicidad, num_cupones):
    num_meses = ten(periodicidad)
    resultado = []
    fecha_ini = fecha_inicial
    for i in range(1, num_cupones + 1):
        fecha_fin = buss_day(add_months(fecha_inicial, num_meses * i))
        resultado.append((fecha_ini, fecha_fin))
        fecha_ini = fecha_fin
    return resultado


def intereses_pata_fija(fechas, nocional, valor_tasa, tipo_tasa='LinAct/360'):
    resultado = []
    for x in zip(nocional, fechas):
        dias = int((x[1][1] - x[1][0]).days)
        interes = x[0] * valor_tasa * dias / 360.0
        resultado.append( (x[0], x[1][0], x[1][1], interes) )
    return resultado


def intereses_pata_flotante(fecha_hoy, fechas, nocional, curva_interpol, tipo_tasa='LinAct/360'):
    resultado = []
    for x in zip(nocional, fechas):
        dias1 = int((x[1][0] - fecha_hoy).days)
        dias2 = int((x[1][1] - fecha_hoy).days)
        df1 = curva_interpol(dias1)
        df2 = curva_interpol(dias2)
        valor_tasa = ((df1/df2)-1)*360/(dias2 - dias1)   #tasa r cuadern
        dias = int((x[1][1] - x[1][0]).days)
        interes = x[0] * valor_tasa * dias / 360.0
        resultado.append( (x[0], x[1][0], x[1][1], interes) )
    return resultado


# VALOR A MINIMIZAR
def valor_swap(tasa_fija, fecha_hoy, fechas, nocional, intereses_plata_flotante, curva_interpol):
    int_pata_fija = intereses_pata_fija(fechas, nocional, tasa_fija)
    pv_fija = valor_presente(fecha_hoy,int_pata_fija,curva_interpol)
    vp_flotante = valor_presente(fecha_hoy,intereses_pata_flotante,curva_interpol)
    return pv_fija - vp_flotante
    #recibo pata fija y pago flotante

def valor_swap_1(fecha_hoy, fechas, nocional, intereses_pata_flotante, curva_interpol):
    def vswap(tasa_fija):
        int_pata_fija = intereses_pata_fija(fechas, nocional, tasa_fija)
        pv_fija = valor_presente(fecha_hoy, int_pata_fija, curva_interpol)
        vp_flotante = valor_presente(fecha_hoy, intereses_pata_flotante, curva_interpol)
        return pv_fija - vp_flotante
    return vswap


def curva(plazos, dfs):
    def curva_interp(plazo):
        log_dfs = []
        for df in dfs:
            log_dfs.append(math.log(df))
        return math.exp(interp1d(plazos, log_dfs, kind='linear')(plazo))
    return curva_interp


def valor_presente(fecha_hoy, intereses, curva_interpol):
    resultado = 0.0
    for interes in intereses:
        plazo = int( (interes[2] - fecha_hoy).days )
        resultado += interes[3] * curva_interpol(plazo)
    return resultado


def get_curva(path_to_file):
    plazos = []
    tasas = []
    with open(path_to_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            plazos.append(row[0])
            tasas.append(row[1])
    plazos = plazos[1:]
    tasas = tasas[1:]
    plazos1 = []
    tasas1 = []
    for plazo in plazos:
        plazos1.append(float(plazo))
    for tasa in tasas:
        tasas1.append(float(tasa))
    print(plazos1)
    print(tasas1)
    return plazos1, tasas1


if __name__ == "__main__":
    get_curva()
