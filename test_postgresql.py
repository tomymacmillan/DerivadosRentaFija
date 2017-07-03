import psycopg2

def open_connection():
    host = 'adiazv-454.postgres.pythonanywhere-services.com'
    user = 'student'
    db = 'der_rf'
    password = 'student_2017'
    port = '10454'
    conn_string = "host="+host+" dbname="+db+" user="+user+" password="+password
    conn_string += " port="+port

    print(conn_string)
    print("Abriendo conexion ...")
    conn = psycopg2.connect(conn_string)
    aux = "Estado de la conexion: "
    if conn.closed == 0:
        aux += "abierta."
    else:
        aux += "cerrada."
    print(aux)
    return conn

def get_mkt_data_example(conn):
    cur = conn.cursor()
    str_query = "SELECT fecha, codigo, valor FROM market_data.end_of_day_values"
    cur.execute(str_query)
    for record in cur:
        print(record)
    cur.close()
    return

def main():
    conn = open_connection()
    get_mkt_data_example(conn)
    conn.close()
    return

main()