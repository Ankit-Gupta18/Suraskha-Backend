import psycopg2
import psycopg2.pool
import os

class DBManager:
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(cls):
        if cls._connection_pool is None:
            try:
                db_config = {
                    'host': os.environ.get("GURU_DB_HOST", ""),
                    'port': os.environ.get("GURU_DB_PORT", ""),
                    'database': os.environ.get("GURU_DB_DATABASE", ""),
                    'user': os.environ.get("GURU_DB_USER", ""),
                    'password': os.environ.get("GURU_DB_PASSWORD", "")
                }
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(10, 10, **db_config)
                print("Initialized database connection pool successfully.")
            except Exception as e:
                print("Error initializing database connection pool.")
                print(e)

    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize()
        return cls._connection_pool.getconn()

    def release_connection(cls, conn):
        cls._connection_pool.putconn(conn)



    def sample_db_function(self, table_name):
        try:
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name};")
                records = cursor.fetchall()
                return records
        except Exception as e:
            print(f"Error: Unable to fetch records from {table_name}.")
            print.error(e)
            return None
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)


    

    @staticmethod
    def get_instance():
        return DBManager()

    def close_connection(self):
        if self._connection_pool:
            self._connection_pool.closeall()
            logger.info("Connection closed.")




