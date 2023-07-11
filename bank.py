import os
from random import randint
from client import Client
from user import User
from queries import *
from data_base import db
from constants import *
from adm import Adm

# REQUISITAR HORARIO EM UM MÉTODO SEPARADO PARA FICAR ATUALIZANDO O HORARIO SEMPRE QUE FOR USÁ-LO

class Bank:
    def __init__(self, cash_initial):
        self.__actual_user = None
        self.__balance = cash_initial

    @property
    def balance(self):
        return self.__balance

    @property
    def actual_user(self):
        return self.__actual_user

    @actual_user.setter
    def actual_user(self, user):
        self.__actual_user = user

    def window_home(self):
        os.system('cls')
        print("\n\n---------- Bem-vindo ao Caixa Eletronico CaiBank ----------\n")
        opt = input("1 ----- Para Clientes \n2 ----- Para Administradores\n\nEscolha a Opcao : ")
        match opt:
            case "1":
                self.select_option_client()
            case "2":
                self.window_login_adm()
            case _:
                print(error_option_invalid)
                os.system("pause")
                self.window_home()

    def select_option_client(self):
        os.system('cls')
        print("\n---------- Selecione Uma Opcao ----------\n")
        opt = input("1 ----- Login\n2 ----- Cadastro\n\nEscolha a Opcao : ")
        match opt:
            case "1":
                self.window_login_client()
            case "2":
                self.window_signup_client()
            case _:
                print(error_option_invalid)
                os.system("pause")
                self.select_option_client()

    def window_login_client(self):
        os.system('cls')
        print('\n-------------- LOGIN --------------\n')
        user_dict = Client.login_user()
        os.system('pause')
        if not user_dict:
            self.window_home()
        self.__actual_user = Client(user_dict)
        self.menu_client()
        if not self.__actual_user.actualize_last_hour_entry():
            self.__actual_user = None
            self.window_home()

    def window_signup_client(self):
        os.system('cls')
        print("\n-----------  CADASTRO -----------\n")
        id_user = User.signup_user()
        if id_user:
            if Client.create_client(id_user=id_user):
                os.system('pause')
                self.menu_client()
        os.system('pause')
        self.window_home()
        return

    def window_login_adm(self):
        os.system('cls')
        print('\n-------------- LOGIN ADM --------------\n')
        user_dict = Adm.login_user()
        os.system('pause')
        if not user_dict:
            self.window_home()
        self.__actual_user = Adm(user_dict)
        self.menu_adm()
        if not self.__actual_user.actualize_last_hour_entry():
            self.__actual_user = None
            self.window_home()

    def menu_adm(self):
        os.system('cls')
        print("\n---------------- MENU ADM ----------------\n")
        print(menu_adm)
        opt = input('OPCAO : ')
        match opt:
            case "1":
                self.__actual_user.show_requisitions()
                self.menu_adm()

            case "2":
                self.__actual_user.delete_client()
                self.menu_adm()

            case "3":
                #self.block_client()
                print('EM BREVE')
                self.menu_adm()

            case "4":
                self.window_home()

    def menu_client(self):
        os.system('cls')
        print("\n---------------- MENU ----------------\n")
        print(menu_client)
        opt = input("OPCAO : ")
        match opt:
            case "1":
                self.__actual_user.withdraw()
                self.menu_client()

            case "2":
                self.__actual_user.deposit()
                self.menu_client()

            case "3":
                self.__actual_user.transfer()
                self.menu_client()

            case "4":
                self.__actual_user.show_balance()
                self.menu_client()

            case "5":
                self.__actual_user.show_historic()
                self.menu_client()

            case "6":
                self.menu_poupanca()
                self.menu_client()

            case "7":
                self.__actual_user.show_user_data()
                self.menu_client()

            case "8":
                self.window_home()

            case _:
                print(error_option_invalid)
                os.system("pause")
                self.menu_client()

    def __update_actual_user(self, id_user):
        personal_data = db.read_query(query=select_join_userdata.format(id_user))[0]
        keys = db.read_columns_names(table='users')[:-1] + db.read_columns_names(table='dados_pessoais')[1:-1]
        personal_data_zip = list(zip(keys, personal_data))
        dict_user = {k: v for k, v in personal_data_zip}
        self.__actual_user = Client(dict_user)

    def menu_poupanca(self):
        os.system('cls')
        print('\n------------- POUPANCA -------------\n')
        poupanca_data = db.read_query(query=f'SELECT * FROM poupancas WHERE id_conta = {self.__actual_user.id_account}')
        if not poupanca_data:
            print('\nCRIANDO POUPANCA....')
            db.execute_query(query=f'INSERT INTO poupancas (saldo, id_conta) '
                                   f'VALUES (0, {self.__actual_user.id_account})')
            os.system('cls')
            self.menu_poupanca()
        self.__actual_user.update_income_poupanca()
        print(menu_poupanca)
        opt = input("\nOPCAO : ")
        match opt:
            case "1":
                self.__actual_user.deposit_poupanca()
                self.menu_poupanca()

            case "2":
                self.__actual_user.withdraw_poupanca()
                self.menu_poupanca()

            case "3":
                self.__actual_user.show_balance_poupanca()
                self.menu_poupanca()

            case "4":
                self.menu_client()

            case _:
                print(error_option_invalid)
                os.system('pause')
                self.menu_poupanca()


def verify_error_input_str(*tupl_name_value):
    for (n, v) in tupl_name_value:
        if v == '':
            print(f'ERROR: {n} INVALIDO')
            return ['']
    return [v for (n, v) in tupl_name_value]
