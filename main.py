from datetime import date
import various_functions as vf


def main():
    fecha = date(2017, 7, 19)#fecha ya en t+2
    check = vf.fechas_swap(fecha,'6M',10)
    """
    for x in check:
        print(x) #imprime fechas
        y = x[1] - x[0] #ya dentro de la tupla resto las fechas
        print(y)
    """
    nocional = []
    for i in range (0,10):
        nocional.append(3000000000.0)
        tasa = 0.034
        intereses = vf.intereses_pata_fija(check, nocional, tasa)
    for x in intereses:
        print(x)

    plazos = [1.0, 30.0, 90.0, 365.0, 730.0, 1095.0, 1460.0, 1825.0, 2190.0]
    dfs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    fecha_hoy = date(2017, 7, 17)
    curva_interp = vf.curva(plazos, dfs)
    print(curva_interp(100.0))
    # vp = valor_presente_pata_fija(fecha_hoy, intereses, curva_interp)






main()
