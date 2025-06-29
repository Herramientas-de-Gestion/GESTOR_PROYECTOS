# Settings/sql_server.py
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=VS1\\INTEL;DATABASE=GESTORTAREASUTP;UID=;PWD='
        )
        cursor=connection.cursor()
        cursor.execute("select @@VERSION")
        row = cursor.fetchone()
        print(row)
        print("Conexión exitosa.")
        return connection
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return None

def get_sqlalchemy_uri():
    print('conexion establecida')
    db_server_name = os.getenv('DB_SERVER_NAME')
    print(db_server_name)
    return (
        f"mssql+pyodbc://@{db_server_name}/Gestor_Proyectos"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
