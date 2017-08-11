from datetime import date
import various_functions_1 as vf
from scipy.optimize import newton


def main():
    fecha = date(2017, 7, 19)
    fechas = vf.fechas_swap(fecha,'6M',10)
    """
    for x in fechas:
        print(x)
        y = x[1]-x[0]
        print(y)
    """
    nocional = []
    for i in range(0, 10):
        nocional.append(3000000000.0)
        tasa = .034
    int_pata_fija = vf.intereses_pata_fija(fechas, nocional, tasa)
    for x in int_pata_fija:
        print(x)

    plazos, dfs = vf.get_curva("./curva_camara_clp.csv")
    # print(plazos)
    # print(dfs)

    fecha_hoy = date(2017, 7, 17)
    curva_interp = vf.curva(plazos, dfs)

    """
    vp_pata_fija = vf.valor_presente(fecha_hoy, int_pata_fija, curva_interp)
    print(vp_pata_fija)
    print()

    int_pata_flotante = vf.intereses_pata_flotante(fecha_hoy, fechas, nocional, curva_interp)
    # for int in int_pata_flotante:
    #     print(int)
    vp_pata_flotante = vf.valor_presente(fecha_hoy, int_pata_flotante, curva_interp)
    print(vp_pata_flotante)
    """
    int_pata_flotante = vf.intereses_pata_flotante(fecha_hoy, fechas, nocional, curva_interp)
    tasa_inicial = .1
    func_vswap = vf.valor_swap_1(fecha_hoy, fechas, nocional, int_pata_flotante, curva_interp)
    print(func_vswap(.0339))
    tasa_pricing = newton(func_vswap, tasa_inicial)
    print(tasa_pricing)


if __name__ == "__main__":
    main()
