import psycopg2
from psycopg2 import OperationalError
try:
    conn = psycopg2.connect(
    dbname="DriveX",
    user="FalconLD",
    password="1234",
    host="localhost",
    port="5432"
    )
    print("Conectado a PostgreSQL")
    conn.close()
    print("Conexión cerrada")
except OperationalError as e:
    print("􎆡 Error de conexión:", e)