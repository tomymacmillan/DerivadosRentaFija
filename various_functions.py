from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from scipy.interpolate import interp1d
import math


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
    for i in range(1, num_cupones+1): # En python el ultimo intervalo es no inclusive
        fecha_fin = buss_day(add_months(fecha_inicial, num_meses * i))
        resultado.append((fecha_ini, fecha_fin))
        fecha_ini = fecha_fin
    return resultado

def intereses_pata_fija(fechas, nocional, valor_tasa, tipo_tasa='LinAct/360'): # El nocional va a ser un vector de nocionales vigintes que va incorporando la amortización. Para el ejemplo de excel es Bullet.
    """
    Vamos a asumir que la amortización es Bullet
    """
    resultado = []
    for x in zip(nocional, fechas):
        dias = int((x[1][1] - x[1][0]).days)
        interes = x[0] * valor_tasa * (dias) / 360.0
        resultado.append((x[0], x[1][0], x[1][1], interes))
    return resultado


def curva(plazos, dfs):
    def curva_interp(plazo):
        log_dfs = []
        for df in dfs: # con numpy podria hacer el log de todo en una sola pasada
            log_dfs.append(math.log(df))
        return math.exp(interp1d(plazos, log_dfs, kind='linear')(plazo))
    return curva_interp

def valor_presente_pata_fija(fecha_hoy, intereses, curva_interpol): #intereses viene de intereses_pata_fija. Fijarme en lo que paso en curva_interpol (ver en main).
    resultado = 0.0 #inicializo double
    for interes in intereses:
        plazo = int((interes[2] - fecha_hoy).days)
        resultado += interes[3] * curva_interpol(plazo)
    return resultado















