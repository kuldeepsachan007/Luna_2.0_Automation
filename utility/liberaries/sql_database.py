import logging
import mysql.connector
from mysql.connector import Error
from os import getenv

logger = logging.getLogger(__name__)


class SQLDatabase:

    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        self.host = host or getenv("DB_HOST", "192.168.158.203")
        self.port = int(port or getenv("DB_PORT", 3306))
        self.user = user or getenv("DB_USER", "kuldeep.sachan")
        self.password = password or getenv("DB_PASSWORD", "K^1d33pXn0!$32025")
        self.database = database or getenv("DB_NAME", "luna")
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            logger.info(f"Connected to MySQL database '{self.database}' at {self.host}:{self.port}")
            return self
        except Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            logger.info(f"Query executed: {query}")
            return cursor.rowcount
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            logger.info(f"Fetched one row for: {query}")
            return result
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            logger.info(f"Fetched {len(results)} rows for: {query}")
            return results
        finally:
            cursor.close()

    def get_tables(self):
        return self.fetch_all("SHOW TABLES")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

if __name__=="__main__":
    sql_data_base = SQLDatabase()
    sql_data_base.connect()

    row = sql_data_base.fetch_all(
        "SELECT * FROM sleep_master_v2 WHERE user_id = 779009"
    )
    print(row)
       