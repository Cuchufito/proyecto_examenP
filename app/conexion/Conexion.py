import psycopg2

class Conexion:

    """Metodo constructor
    """
    def __init__(self):
        dbname = "taller_db"
        user = "postgres"
        password = "Admin"
        host = "127.0.0.1"
        port = 5432
        #self.con = psycopg2.connect("dbname=veterinariadb user=postgres host=localhost password=1873")
        self.con = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    """getConexion

        retorna la instancia de la base de datos
    """
    def getConexion(self):
        return self.con