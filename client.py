import mysql.connector
from data_base import db
from queries import *
from constants import *
from tabulate import tabulate
from datetime import datetime
from random import randint
from user import User
import re 
import decimal as dec
import os


class Client(User):
    def __init__(self, user_dict):
        super().__init__(id_user=user_dict['id_user'], email=user_dict['email'],
                         password=user_dict['password'], last_hour_entry=user_dict['ultimo_horario_entrada'])

        personal_dict = read_personal_dict(self.id_user)
        if not personal_dict:
            Client.create_client()
        personal_dict = read_personal_dict(self.id_user)
        account_dict = read_account_dict(self.id_user)
        self._id_account = account_dict['id_conta']
        self._num_account = account_dict['numero_conta']
        self._cpf = personal_dict['cpf']
        self._date_birth = personal_dict['data_nascimento']
        self._name = personal_dict['nome_completo']

    @property
    def id_user(self):
        return self._id_user

    @property
    def id_account(self):
        return self._id_account

    @property
    def last_hour_entry(self):
        return self._last_hour_entry
    
    @classmethod
    def create_client(cls, id_user):
        try:
            name = input('Nome Completo : ')
            cpf = input('CPF (Formato : XXX.XXX.XXX-XX) : ')
            if not verify_cpf(cpf=cpf):
                raise ValueError('CPF no formato errado')
            personal_dict = db.dict_columns(table='dados_pessoais', condition=f'cpf = "{cpf}"')
            if personal_dict:
                print('ERROR : CPF ja cadastrado sistema')
                return False
            date_birth = input('Data de Nascimento (Formato YYYY-MM-DD) : ' )
            if not verify_date_birth(date_birth=date_birth):
                raise ValueError('Data de Nascimento no Formato Errado')
            
            if verify_unwritten(cpf) or verify_unwritten(name) or verify_unwritten(date_birth):
                print('ERROR : Insira dados não nulos')
                return False
            db.insert_into_table(table='dados_pessoais', columns='cpf, nome_completo, data_nascimento, id_user',
                                 values=f'"{cpf}", "{name}", "{date_birth}", "{id_user}"')
            
            def generate_num_account():
                while True:
                    num_part1 = randint(1, 999999)
                    num_part2 = randint(1, 99)
                    num_account = '{:06}'.format(num_part1) + '{:02}'.format(num_part2)
                    unique = not db.read_query(query=f'SELECT * FROM contas WHERE numero_conta = {num_account}')
                    if unique: break
                return num_account
            num_account = generate_num_account()
            db.insert_into_table(table='contas', columns='numero_conta, saldo, id_user', 
                                 values=f'"{num_account}", {0}, {id_user}')
            return True
            
        except Exception as err:
            print(f'ERROR : {err}')
            
    def withdraw(self):
        print('\n---------------- SAQUE ----------------\n\n')
        try:
            draw = float(input('Escolha o valor que deseja sacar : R$ '))
        except ValueError:
            print("Insira no formato (1000.00)")
            self.withdraw()
            return
        balance = self.consult_balance()
        if draw > balance:
            print('ERROR : Voce nao tem saldo suficiente')
        elif draw <= 0:
            print('ERROR : Valor Invalido')
        else:
            self.update_balance(increment=draw, sign='-', id_user=self._id_user)
            print('SAQUE CONCLUIDO COM SUCESSO !!!')
            self.__create_operation(operation="Saque", value=draw)
        print("\n")
        os.system('pause')
        return

    def deposit(self):
        print('\n---------------- DEPOSITO ----------------\n\n')
        try:
            deposit = float(input("Valor do Deposito : "))
        except ValueError:
            print("Insira no formato (1000.00)")
            self.deposit()
            return
            
        if deposit <= 0:
            print('ERROR : Valor Invalido')
        elif deposit > limit_deposit:
            self.__create_operation(operation="Requisicao De Deposito", value=deposit, approved='NAO')
            print(f'ERROR : Valor maior que o limite R$ {limit_deposit} por deposito\n'
                  f'Sua Requisicao Foi Enviada P/ Administracao !!!\n'
                  f'Contate o SUPORTE para mais informacoes')
        else:
            self.update_balance(increment=deposit, sign='+', id_user=self._id_user)
            print('DEPOSITO CONCLUIDO !!!')
            self.__create_operation(operation="Deposito", value=deposit)
        print("\n")
        os.system('pause')
        return

    def show_balance(self):
        print('\n---------------- SALDO ----------------\n\n')
        balance = self.consult_balance()
        print(f'SALDO : R$ {balance}')
        print("\n")
        os.system('pause')
        return

    def transfer(self):
        print('\n---------------- TRANSFERENCIA ----------------\n\n')
        try:
            num_account = input('Qual a conta que deseja transferir ? (8 Digitos): ')
            if not verify_account_number(num_account=num_account):
                raise ValueError
        except ValueError:
            print("Formato Invalido de Conta")
            os.system('pause')
            return
        
        dict_benef = db.dict_columns(table='contas', condition=f'numero_conta = {num_account}')
        if not dict_benef:
            print("ERROR : Nao Existe Essa Conta no Sistema")
        else:
            id_user_benef = dict_benef['id_user']
            value_t = float(input('Insira valor a transferir : R$ '))
            if value_t <= 0:
                print('ERROR : Valor Invalido')
            elif value_t > limit_transfer:
                print(f'ERROR : Valor maior que o limite R$ {limit_transfer} por transferencia')
            else:
                self.update_balance(increment=value_t, sign='+', id_user=id_user_benef)
                self.update_balance(increment=value_t, sign='-', id_user=self._id_user)
                self.__create_operation(operation='Transferencia', value=value_t, id_user_benef=id_user_benef)
                print('TRANSFERENCIA REALIZADA !!!')
        print("\n")
        os.system('pause')
        return

    def consult_balance(self):
        account_dict = db.dict_columns(table='contas', condition=f'id_conta = {self._id_account}')
        return account_dict['saldo']
    
    
    @staticmethod    
    def update_balance(increment, sign, id_user):
        db.update_column(table='contas', column='saldo', value=f'saldo {sign} {increment}',
                         condition=f'id_user = {id_user}')
            
    @staticmethod
    def update_balance_poupanca(increment, sign, id_account):
        db.update_column(table='poupancas', column='saldo', value=f'saldo {sign} {increment}',
                         condition=f'id_conta = {id_account}')

    def __create_operation(self, operation, value=None, id_user_benef=None, approved='SIM'):
        db.execute_query(query=create_operation.format(operation, self._id_account, time_now(), value, approved))
        if operation == 'Transferencia':
            id_account_benef = db.dict_columns(table='contas', condition=f'id_user = {id_user_benef}')['id_conta']
            id_last_operation = db.dict_all(table='operacoes', 
                                            condition=f'id_conta_operada = {self.id_account}')[-1]['id_operacao']
            db.execute_query(query=create_transfer.format(id_account_benef, self._id_account, id_last_operation))
        return

    def show_historic(self):
        print('\n---------------- EXTRATO ----------------\n\n')
        table = db.read_query(query=read_operations.format(self._id_account))
        table = list(map(signal_operation, table))
        headers = ["Tipo da Operacao", "Valor Operacao", "Data e Hora da Operacao", "Aprovado"]
        print(tabulate(table, headers=headers))
        print("\n")
        os.system("pause")
        return

    def show_user_data(self):
        print('\n---------------- MEUS DADOS ----------------\n')
        print(f'NOME : {self._name}\nCPF : {self._cpf}\nCONTA : {self._num_account}\n')
        os.system('pause')
        
    # PAREI AQUI
        
    def update_income_poupanca(self):
        last_hour_obj = self._last_hour_entry
        if type(last_hour_obj) == str:
            last_hour_obj = datetime.strptime(self._last_hour_entry, "%Y-%m-%d %H:%M:%S")
        time_now_obj = datetime.strptime(time_now(), "%Y-%m-%d %H:%M:%S")
        time_diff = time_now_obj - last_hour_obj
        self._last_hour_entry = time_now()
        self.__actualize_last_hour()
        balance_p = float(db.read_query(query=read_balance_p.format(self._id_account))[0][0])
        time_diff_h = time_diff.total_seconds() / (60*60)
        income = balance_p * rate_poupanca * time_diff_h
        db.update_column(table='poupancas', column='saldo',
                         value=balance_p+income, condition=f'id_conta = {self._id_account}')

    def deposit_poupanca(self):
        print('\n---------------- DEPOSITO POUPANCA ----------------\n\n')
        try:
            deposit = float(input('Insira o valor que deseja depositar : R$ '))
            if not verify_number_value(number=deposit):
                raise ValueError('Deposito no Formato Errado')
        except ValueError:
            self.deposit_poupanca()
            return
        balance_acc = float(db.read_query(query=read_balance.format(self._id_user))[0][0])
        if deposit <= 0 or deposit > balance_acc:
            print('ERROR : Valor Invalido ou Saldo Na Conta Insuficiente')
        else:
            self.update_balance_poupanca(increment=deposit, sign='+', id_account=self._id_account)
            self.update_balance(increment=deposit, sign='-', id_user=self._id_user)
            print('DEPOSITO REALIZADO COM SUCESSO')

        os.system('pause')
        return

    def withdraw_poupanca(self):
        print('\n---------------- SAQUE PARA CONTA ----------------\n\n')
        try:
            draw = float(input('Escolha o valor que deseja sacar : R$ '))
            if not verify_number_value(number=draw):
                raise ValueError('Saque no Formato Errado')
        except ValueError:
            self.withdraw_poupanca()
            return
        balance_p = float(db.read_query(query=read_balance_p.format(self._id_account))[0][0])
        if draw <= 0 or draw >= balance_p:
            print('ERROR : Valor Invalido ou Saldo Insuficiente')
        else:
            self.update_balance_poupanca(increment=draw, sign='-', id_account=self._id_account)
            self.update_balance(increment=draw, sign='+', id_user=self._id_user)
            print('SAQUE REALIZADO COM SUCESSO')

        os.system('pause')
        return

    def show_balance_poupanca(self):
        print('\n---------------- SALDO POUPANCA ----------------\n\n')
        balance = db.read_query(query=read_balance_p.format(self._id_account))
        print(f'SALDO : R$ {balance[0][0]}')
        os.system('pause')
        return

    def __actualize_last_hour(self):
        db.update_column(table='users', column='ultimo_horario_entrada',
                         value=f'"{time_now()}"', condition=f'id_user = {self._id_user}')
        self._last_hour_entry = time_now()


def signal_operation(tupl):
        if tupl[0] in ['Transferencia', 'Saque']:
            return tupl[0], f'R$ -{tupl[1]}', tupl[2], tupl[3]

        elif tupl[0] in ['Deposito', 'Requisicao De Deposito']:
            return tupl[0], f'R$ +{tupl[1]}', tupl[2], tupl[3]

def read_account_dict(id_user):
    try:
        account_dict = db.dict_columns(table='contas', condition=f'id_user = {id_user}')
        return account_dict
    except mysql.connector.Error as err:
        print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
    except Exception as err:
        print(f'ERROR : {err}')
        
def read_personal_dict(id_user):
    try:
        personal_dict = db.dict_columns(table='dados_pessoais', condition=f'id_user = {id_user}')
        return personal_dict
    except mysql.connector.Error as err:
        print(f'ERROR : Conexao com o Banco de Dados apresentou o erro {err}')
    except Exception as err:
        print(f'ERROR : {err}')
        