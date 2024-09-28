import psycopg2
import psycopg2.pool
import os
import asyncio
from typing import List, Tuple, Optional
from datetime import datetime


class DBManager:
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        if self._connection_pool is None:
            try:
                db_config = {
                    'host': os.environ.get("SURAKSHA_DB_HOST", "localhost"),
                    'port': os.environ.get("SURAKSHA_DB_PORT", "5432"),
                    'database': os.environ.get("SURAKSHA_DB_DATABASE", "your_db"),
                    'user': os.environ.get("SURAKSHA_DB_USER", "your_user"),
                    'password': os.environ.get("SURAKSHA_DB_PASSWORD", "your_password")
                }
                self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    **db_config
                )
                print("Initialized database connection pool successfully.")
            except Exception as e:
                print("Error initializing database connection pool.")
                print(e)

    def get_connection(self):
        if self._connection_pool is None:
            self.initialize()
        return self._connection_pool.getconn()

    def release_connection(self, conn):
        if self._connection_pool:
            self._connection_pool.putconn(conn)

    def sample_db_function(self, table_name: str):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name};")
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error: Unable to fetch records from {table_name}.")
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.release_connection(connection)

    def save_message_sync(self, sender_id: int, receiver_id: int, message: str):
        """
        Synchronous method to save a chat message to the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO chat_messages (sender_id, receiver_id, message, timestamp)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (sender_id, receiver_id, message))
            connection.commit()
            print(f"Message from User {sender_id} to User {receiver_id} saved successfully.")
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error saving message: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.release_connection(connection)

    def get_chat_history_sync(self, sender_id: int, receiver_id: int) -> Optional[List[Tuple[int, str, datetime]]]:
        """
        Synchronous method to retrieve chat history between two users.
        Returns a list of tuples containing sender_id, message, and timestamp.
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            select_query = """
                SELECT sender_id, message, timestamp 
                FROM chat_messages 
                WHERE (sender_id = %s AND receiver_id = %s) 
                OR (sender_id = %s AND receiver_id = %s)
                ORDER BY timestamp ASC
            """
            cursor.execute(select_query, (sender_id, receiver_id, receiver_id, sender_id))
            records = cursor.fetchall()
            return records  # Each record is a tuple: (sender_id, message, timestamp)
        except Exception as e:
            print(f"Error fetching chat history between User {sender_id} and User {receiver_id}: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.release_connection(connection)

    async def save_message(self, sender_id: int, receiver_id: int, message: str):
        """
        Asynchronous wrapper for saving a message using run_in_executor to prevent blocking.
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_message_sync, sender_id, receiver_id, message)

    async def get_chat_history(self, sender_id: int, receiver_id: int) -> Optional[List[Tuple[str, str]]]:
        """
        Asynchronous wrapper for retrieving chat history using run_in_executor to prevent blocking.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_chat_history_sync, sender_id, receiver_id)

    @staticmethod
    def get_instance():
        return DBManager()

    def close_connection_pool(self):
        """
        Close all connections in the pool.
        """
        if self._connection_pool:
            self._connection_pool.closeall()
            print("Database connection pool closed.")
