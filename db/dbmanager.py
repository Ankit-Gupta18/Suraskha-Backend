import psycopg2
import psycopg2.pool
import os
import pandas as pd

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

                if record:
                    # Map the record to a dictionary
                    user = {
                        "id": record[0],
                        "name": record[1],
                        "aadhaar_number": record[2],
                        "state": record[3],
                        "age_group": record[4],
                        "gender": record[5],
                        "phone_number": record[6],
                        "email": record[7],
                        "avatar": record[8]
                    }
                    return user
                else:
                    return None
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

    def update_user_location(self, aadhaar_number: str, latitude: float, longitude: float, table_name: str = "user_auth_db"):
        try:
            # Query to update latitude and longitude for the user identified by aadhaar_number
            query = f"""
                UPDATE {table_name}
                SET latitude = %s, longitude = %s, updated_at = CURRENT_TIMESTAMP
                WHERE aadhaar_number = %s;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (latitude, longitude, aadhaar_number))
                connection.commit()
                return {"status": "success", "message": "Location updated successfully"}
        except Exception as e:
            print(f"Error: Unable to update location for aadhaar_number {aadhaar_number}.")
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

                if record:
                    # Map the tuple to a dictionary
                    police = {
                        "id": record[0],
                        "name": record[1],
                        "police_id": record[2],
                        "police_station_address": record[3],
                        "phone_number": record[4],
                        "email": record[5],
                        "id_card": record[6],
                        "avatar": record[7]
                    }
                    return police
                else:
                    return None
        except Exception as e:
            print(f"Error: Unable to fetch police with phone number {phone_number}.")
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

    def insert_user_contact(self, payload: dict, table_name: str = "user_contacts"):
        try:
            # Extracting the payload values
            aadhaar_number = payload.get("aadhaar_number")
            name = payload.get("name")
            relation = payload.get("relation")
            phone_number = payload.get("phone_number")
            email = payload.get("email")
            status = payload.get("status")
            priority = payload.get("priority")
            latitude = payload.get("latitude")
            longitude = payload.get("longitude")
            
            query = f"""
                INSERT INTO {table_name} 
                (aadhaar_number, name, relation, phone_number, email, status, priority, latitude, longitude, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (
                    aadhaar_number, name, relation, phone_number, email, status, priority, latitude, longitude
                ))
                connection.commit()
                return {"status": "success", "message": "User contact inserted successfully"}
        except Exception as e:
            print(f"Error: Unable to insert contact into {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def fetch_all_user_contacts(self, table_name: str = "user_contacts"):
        try:
            query = f"""
                SELECT name, relation, phone_number, email, status, priority
                FROM {table_name};
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query)
                # Fetch all results
                result = cursor.fetchall()

                # Format the result into a list of dictionaries
                user_contacts = [
                    {
                        "name": row[0],
                        "relation": row[1],
                        "phone_number": row[2],
                        "email": row[3],
                        "status": row[4],
                        "priority": row[5]
                    } for row in result
                ]

                return {"status": "success", "data": user_contacts}
        except Exception as e:
            print(f"Error: Unable to fetch user contacts from {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)
            
    def delete_user_contact_by_phone(self, phone_number: str, table_name: str = "user_contacts"):
        try:
            # SQL query to delete the contact based on the phone number
            query = f"""
                DELETE FROM {table_name}
                WHERE phone_number = %s;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (phone_number,))
                connection.commit()

                # Check if any rows were affected (i.e., if the contact existed)
                if cursor.rowcount == 0:
                    return {"status": "error", "message": "No contact found with the given phone number"}
                return {"status": "success", "message": "User contact deleted successfully"}
        except Exception as e:
            print(f"Error: Unable to delete contact from {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def update_user_contact_by_phone(self, phone_number, payload: dict, table_name: str = "user_contacts"):
        try:
            # Extracting the values from the payload
            aadhaar_number = payload.get("aadhaar_number")
            name = payload.get("name")
            relation = payload.get("relation")
            new_phone_number = payload.get("new_phone_number")
            email = payload.get("email")
            status = payload.get("status")
            priority = payload.get("priority")
            latitude = payload.get("latitude")
            longitude = payload.get("longitude")

            # SQL query to update the user contact details
            query = f"""
                UPDATE {table_name}
                SET aadhaar_number = %s,
                    name = %s,
                    relation = %s,
                    phone_number = %s,
                    email = %s,
                    status = %s,
                    priority = %s,
                    latitude = %s,
                    longitude = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE phone_number = %s;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (
                    aadhaar_number, name, relation, new_phone_number, email, status, priority, latitude, longitude, phone_number
                ))
                connection.commit()

                # Check if any rows were affected (i.e., if the contact existed)
                if cursor.rowcount == 0:
                    return {"status": "error", "message": "No contact found with the given phone number"}
                return {"status": "success", "message": "User contact updated successfully"}
        except Exception as e:
            print(f"Error: Unable to update contact in {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def fetch_phone_by_priority(self, priority, table_name: str = "user_contacts"):
        try:
            query = f"""
                SELECT phone_number 
                FROM {table_name} 
                WHERE priority = %s;
            """
            
            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (priority,))
                result = cursor.fetchall()
                
                if result:
                    phone_numbers = [row[0] for row in result]
                    return {"status": "success", "phone_numbers": phone_numbers}
                else:
                    return {"status": "failed", "message": "No phone numbers found with given priority"}
        except Exception as e:
            print(f"Error: Unable to fetch phone numbers from {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    import math

    def fetch_nearest_phone_numbers(self, latitude: float, longitude: float, table_name: str = "user_contacts", limit: int = 3):
        try:
            # Haversine formula to calculate distance between two lat/long points
            query = f"""
                SELECT phone_number, (
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(latitude)) * 
                        cos(radians(longitude) - radians(%s)) + 
                        sin(radians(%s)) * sin(radians(latitude))
                    )
                ) AS distance,
                latitude, longitude
                FROM {table_name}
                ORDER BY distance ASC
                LIMIT %s;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (latitude, longitude, latitude, limit))
                result = cursor.fetchall()

                # Process the result to extract the phone numbers
                phone_numbers = [{"phone_number": row[0], "distance_km": row[1], "latitude": row[2], "longitude": row[3]} for row in result]
                user_contacts_locations = [{"latitude": row[2], "longitude": row[3]} for row in result]

                return {"status": "success", "data": phone_numbers, "user_contacts_locations": user_contacts_locations}
        except Exception as e:
            print(f"Error: Unable to fetch nearest phone numbers from {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)

    def fetch_nearest_police_numbers(self, latitude: float, longitude: float, table_name: str = "police_auth_db", limit: int = 3):
        try:
            # Haversine formula to calculate distance between two lat/long points
            query = f"""
                SELECT phone_number, (
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(latitude)) * 
                        cos(radians(longitude) - radians(%s)) + 
                        sin(radians(%s)) * sin(radians(latitude))
                    )
                ) AS distance,
                latitude, longitude
                FROM {table_name}
                ORDER BY distance ASC
                LIMIT %s;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (latitude, longitude, latitude, limit))
                result = cursor.fetchall()

                # Process the result to extract the phone numbers
                police_numbers = [{"phone_number": row[0], "distance_km": row[1], "latitude": row[2], "longitude": row[3]} for row in result]
                police_locations = [{"latitude": row[2], "longitude": row[3]} for row in result]

                return {"status": "success", "data": police_numbers, "locations": police_locations}
        except Exception as e:
            print(f"Error: Unable to fetch nearest police phone numbers from {table_name}.")
            print(e)
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)


    def fetch_location_ratings(self, table_name: str = "location_ratings"):
        try:
            # SQL query to fetch location ratings with additional columns
            query = f"""
            SELECT location, state, latitude, longitude, rating 
            FROM {table_name} ORDER BY rating DESC;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                # Fetch column names from cursor
                column_names = [desc[0] for desc in cursor.description]

                # Create a DataFrame from the fetched rows
                location_rating_table = pd.DataFrame(rows, columns=column_names)

                return location_rating_table
        except Exception as e:
            print(f"Error: Unable to fetch data from {table_name}.")
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            self.release_connection(connection)


    def insert_or_update_location_rating(self, location: str, state: str, latitude: float, longitude: float, new_rating: float, table_name: str = "location_ratings"):
        try:
            # SQL query to insert or update location rating
            query = f"""
            INSERT INTO {table_name} (location, state, latitude, longitude, rating, frequency)
            VALUES (%s, %s, %s, %s, %s, 1)
            ON CONFLICT (latitude, longitude)
            DO UPDATE 
            SET 
                rating = (({table_name}.rating * {table_name}.frequency) + EXCLUDED.rating) / ({table_name}.frequency + 1),
                frequency = {table_name}.frequency + 1
            RETURNING id, location, state, latitude, longitude, rating, frequency;
            """

            # Open the connection and execute the query
            with self.get_connection() as connection, connection.cursor() as cursor:
                cursor.execute(query, (location, state, latitude, longitude, new_rating))
                updated_row = cursor.fetchone()

                # Fetch column names from cursor
                column_names = [desc[0] for desc in cursor.description]

                # Create a DataFrame from the fetched row
                updated_location_rating = pd.DataFrame([updated_row], columns=column_names)

                return updated_location_rating

        except Exception as e:
            print(f"Error: Unable to insert or update data in {table_name}.")
            print(e)
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
            print("Connection closed.")




