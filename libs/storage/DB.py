import psycopg2
from libs.storage.login.login import (
    hostname,
    username,
    password,
    database,
    port
)

 
class DBStructure:
    """
        Class used to connect into the database and do
        all the respective operations
    """
    def __init__(self):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database
        self.port = port

    def __db_conect(self):
        try:
            self.connector = psycopg2.connect(host=self.hostname, user=self.username, database=self.database, password=self.password, port=self.port)
            self.cursor = self.connector.cursor()
        except:
            raise ConnectionError()

    def db_create(self, table_name: str, data: dict[str, str]):
        self.__db_conect()
        clause = f'INSERT INTO {table_name}({", ".join([column for column in data.keys()])}) VALUES('
        clause += ", ".join([f"'{data[key]}'" for key in data.keys()]) + ')'
        with self.cursor as session:
            session.execute(clause)
            self.connector.commit()

    def db_read(self, table_name: str, filters: dict or None = None):
        self.__db_conect()
        clause = f'SELECT * FROM {table_name}'
        if filters:
            control = 0
            for key in filters.keys():
                if control == 0:
                    clause += f' WHERE {key} = {filters[key]}'
                    control += 1
                elif control != len(filters.keys()):
                    clause += f' AND {key} = {filters[key]}'
                    control += 1
        with self.cursor as session:
            session.execute(clause)
            self.results = session.fetchall();


    def db_update(self, table_name: str, occurrence: dict or None = None):
        self.__db_conect()
        clause = f'UPDATE {table_name} SET {occurrence.get("update", "-")} = {occurrence.get("value", "-")}'
        clause += f' WHERE {occurrence.get("key", "-")} = {occurrence.get("key_value", "-")}'
        with self.cursor as session:
            session.execute(clause)
            self.connector.commit()

    def db_delete(self, table_name: str, occurrence: dict or None = None):
        self.__db_conect()
        clause = f'DELETE FROM {table_name}'
        clause += f' WHERE {occurrence.get("key", "-")} = {occurrence.get("key_value", "-")}'
        clause += f' RETURNING {occurrence.get("key", "-")}'
        with self.cursor as session:
            session.execute(clause)
            self.connector.commit()


client = {
    'phone_number': '19998442741',
    'name': 'Leandro'
}



# Documentation: https://www.tutorialspoint.com/python_data_access/python_postgresql_select_data.html
