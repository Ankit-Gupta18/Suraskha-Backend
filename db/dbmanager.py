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
                    'host': os.environ.get("SURAKSHA_DB_HOST", ""),
                    'port': os.environ.get("SURAKSHA_DB_PORT", ""),
                    'database': os.environ.get("SURAKSHA_DB_DATABASE", ""),
                    'user': os.environ.get("SURAKSHA_DB_USER", ""),
                    'password': os.environ.get("SURAKSHA_DB_PASSWORD", "")
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

    def get_user_by_phone(self, phone_number):
        try:
            with self.get_connection() as connection, connection.cursor() as cursor:
                query = "SELECT * FROM user_auth_db WHERE phone_number = %s"
                cursor.execute(query, (phone_number,))
                record = cursor.fetchone()
                return record
        except Exception as e:
            print(f"Error: Unable to fetch user with phone number {phone_number}.")
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def insert_user_auth(self, payload: dict, table_name: str = "user_auth_db"):
        try:
            # Extracting the payload values
            name = payload.get("name")
            adhaar_number = payload.get("aadhaar_number")
            state = payload.get("state")
            age_group = payload.get("age_group")
            gender = payload.get("gender")
            phone_number = payload.get("phone_number")
            email = payload.get("email")
            
            query = f"""
                INSERT INTO {table_name} (name, aadhaar_number, state, age_group, gender, phone_number, email, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (name, adhaar_number, state, age_group, gender, phone_number, email))
                connection.commit()
                return {"status": "success", "message": "Record inserted successfully"}
        except Exception as e:
            print(f"Error: Unable to insert record into {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    
    def get_police_by_phone(self, phone_number):
        try:
            with self.get_connection() as connection, connection.cursor() as cursor:
                query = "SELECT * FROM police_auth_db WHERE phone_number = %s"
                cursor.execute(query, (phone_number,))
                record = cursor.fetchone()
                return record
        except Exception as e:
            print(f"Error: Unable to fetch user with phone number {phone_number}.")
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def insert_police_auth(self, payload: dict, table_name: str = "police_auth_db"):
        try:
            # Extracting the payload values
            name = payload.get("name")
            police_id = payload.get("police_id")
            police_station_address = payload.get("police_station_address")
            phone_number = payload.get("phone_number")
            email = payload.get("email")
            id_card = payload.get("id_card")
            
            query = f"""
                INSERT INTO {table_name} 
                (name, police_id, police_station_address, phone_number, email, id_card, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (name, police_id, police_station_address, phone_number, email, id_card))
                connection.commit()
                return {"status": "success", "message": "Record inserted successfully"}
        except Exception as e:
            print(f"Error: Unable to insert record into {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def insert_feedback(self, payload: dict, table_name: str = "feedback_db"):
        try:
            # Extracting the payload values
            name = payload.get("name")
            email = payload.get("email")
            feedback = payload.get("feedback")
            stars = payload.get("stars")
            
            query = f"""
                INSERT INTO {table_name} 
                (name, email, feedback, stars, created_at, updated_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (name, email, feedback, stars))
                connection.commit()
                return {"status": "success", "message": "Feedback inserted successfully"}
        except Exception as e:
            print(f"Error: Unable to insert feedback into {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
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
            print("Connection closed.")




