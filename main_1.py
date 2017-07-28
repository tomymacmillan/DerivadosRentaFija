from datetime import date
import various_functions_1 as vf


def main():
    fecha = date(2017, 7, 19)
    check = vf.fechas_swap(fecha,'6M',10)
    """
    for x in check:
        print(x)
        y = x[1]-x[0]
        print(y)
    """
    nocional = []
    for i in range(0, 10):
        nocional.append(3000000000.0)
        tasa = .034
    intereses = vf.intereses_pata_fija(check, nocional, tasa)
    for x in intereses:
        print(x)

    plazos, dfs = vf.get_curva("./curva_camara_clp.csv")
    # print(plazos)
    # print(dfs)

    fecha_hoy = date(2017, 7, 17)
    curva_interp = vf.curva(plazos, dfs)

    vp = vf.valor_presente_pata_fija(fecha_hoy, intereses, curva_interp)
    print(vp)

if __name__ == "__main__":
    main()
