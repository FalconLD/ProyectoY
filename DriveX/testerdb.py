import psycopg
from psycopg import OperationalError
try:
    conn = psycopg.connect(
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