import mysql.connector
import queries


class DataBase:
    def __init__(self, user, password, host, database, ssl_ca) -> None:
        self.__create_connection(user, password, host, database, ssl_ca)
        self.__cursor = self.__connection.cursor()

    def __create_connection(self, user, password, host, database, ssl_ca):
        connection = None

        try:
            connection = mysql.connector.connect\
                (user=f"{user}", password=f"{password}",
                 host=f"{host}", port=3306,
                 database=f"{database}"
                 )
        except NameError as e:
            print(e)

        self.__connection = connection

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')

    def read_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
            return False
        return result
    
    def dict_all(self, table, condition):
        list_data = self.read_query(query=f'SELECT * FROM {table} WHERE {condition}')
        list_data_dict = list(map(convert_to_dict, list_data))
        return list_data_dict


    def read_columns_names(self, table):
        self.cursor.execute(queries.read_columns.format(table))
        result = self.cursor.fetchall()
        return [col[0] for col in result]
    
    def insert_into_table(self, table, columns, values):
        db.execute_query(query=f'INSERT INTO {table} ({columns}) VALUES ({values}) ')


    def update_column(self, table, column, value, condition=True):
        self.execute_query(query=f'UPDATE {table} SET {column} = {value} WHERE {condition}')

    def dict_all(self, table, condition):
        list_data = self.read_query(query=f'SELECT * FROM {table} WHERE {condition}')
        keys = self.read_columns_names(table)
        list_data_dict = [convert_to_dict(keys=keys, values=data) for data in list_data]
        return list_data_dict
    
    def dict_columns(self, table, condition):
        data = self.read_query(query=f'SELECT * FROM {table} WHERE {condition}')
        if not data:
            return []
        keys = self.read_columns_names(table)
        dict_data = convert_to_dict(values=data[0], keys=keys)
        return dict_data
        

db = DataBase(user="caina", password="Mabare203022@",
              host="caibank.mysql.database.azure.com", database="caibank",
              ssl_ca="DigiCertGlobalRootCA.crt.pem")


def convert_to_dict(keys, values):
    dict_data = {key: value for key, value in zip(keys, values)}
    return dict_data

