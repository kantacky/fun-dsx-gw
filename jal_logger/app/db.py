from config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD
import psycopg

class Database:

    def __init__(self, database_name):
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.database = database_name

    def get_connection(self) -> psycopg.connect:
        return psycopg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database
        )
