import mysql.connector
from constants import *
from data_base import db


class User:
    def __init__(self, id_user, email, password, last_hour_entry) -> None:
        self._id_user = id_user
        self._email = email
        self._password = password
        self._last_hour_entry = last_hour_entry

    @classmethod
    def login_user(cls):
        try:
            email = input('Email : ')
            user_dict = db.dict_columns(table='users', condition=f'email = "{email}"')
            if not user_dict:
                print('ERROR : EMAIL nao existe no sistema')
                return []
            password = input('Senha : ')
            if password != user_dict['password']:
                print('ERROR : SENHA invalida')
                return []
            return user_dict
        except mysql.connector.Error as err:
            print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
        except Exception as err:
            print(f'ERROR : {err}')
            
    @classmethod
    def signup_user(cls):
        try:
            email = input('Email : ')
            user_dict = db.dict_columns(table='users', condition=f'email = "{email}"')
            if user_dict:
                print('ERROR : EMAIL ja existe no sistema\nComplete seu Cadastro : \n')
                return user_dict['id_user']
            password_1 = input("Crie uma senha : ")
            password_2 = input("Confirme a senha : ")
            if password_1 != password_2:
                while password_1 != password_2:
                    print("ERROR : Senhas Diferentes, Tente Novamente")
                    password_1 = input("Crie uma senha : ")
                    password_2 = input("Confirme a senha : ")
                    
            if verify_unwritten(password_2) or verify_unwritten(email):
                print('ERROR : Insira email ou senha validos')
                return False
            db.insert_into_table(table='users', columns='email, password, ultimo_horario_entrada',
                                 values=f'"{email}", "{password_2}", "{time_now()}"')
            user_dict = db.dict_columns(table='users', condition=f'email = "{email}"')

            return user_dict['id_user']
        
        except mysql.connector.Error as err:
            print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
            
        except Exception as err:
            print(f'ERROR : {err}')


    def actualize_last_hour_entry(self):
        try:
            db.update_column(table='users', column='ultimo_horario_entrada',
                             value=f'"{time_now()}"', condition=f'users.id_user = {self.__id_user}')
            return True
        except mysql.connector.Error as err:
            print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
            return False


