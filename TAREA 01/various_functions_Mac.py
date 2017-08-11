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

def curva(plazos, dfs):
    def curva_interp(plazo):
        log_dfs = []
        for df in dfs:
            log_dfs.append(math.log(df))
        return math.exp(interp1d(plazos, log_dfs, kind='linear')(plazo))
    return curva_interp

# Importar Datos
def importar_csv(path_to_file):
    tenors = []
    tasas = []
    with open(path_to_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            tenors.append(row[0])
            tasas.append(row[1])
    tenors = tenors[0:]
    tasas = tasas[0:]
    tasas_float = []
    for i in tasas:
        tasas_float.append(float(i)*100)
    return tenors, tasas_float

if __name__ == "__main__":
    importar_csv()
