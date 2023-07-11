import os
from client import User, Client
from queries import *
from data_base import db
from constants import error_option_invalid
from tabulate import tabulate


class Adm(User):
    def __init__(self, user_dict):
        super().__init__(id_user=user_dict['id_user'], email=user_dict['email'],
                         password=user_dict['password'], last_hour_entry=['ultimo_horario_entrada'])

    @classmethod
    def login_user(cls):
        user_dict = super().login_user()
        if not user_dict:
            return []
        elif user_dict['adm'] == 'SIM':
            return user_dict
        else:
            print('ERROR : Voce nao tem permissao de Administrador')
            return []

    def delete_client(self):
        print('\n---------------- DELECAO DE CONTA ----------------\n\n')
        email_delete = input('Email Do Usuario A Deletar : ')
        print('ATENCAO : Esse Usuario Sera Deletado para SEMPRE')
        opt = input('Deseja confimrar deleção ? (S/N) : ')
        if opt == 'S':
            id_user = db.read_query(query=search_id_with_email.format(email_delete))
            if not id_user:
                print('Usuario Nao Encontrado')
            else:
                id_user = id_user[0][0]
                id_account = db.read_query(query=consult_id_account.format(id_user))[0][0]
                if id_account:
                    db.execute_query(query=delete_id_account.format('poupancas', id_account))
                id_account = db.read_query(query=consult_id_account.format(id_user))[0][0]
                db.execute_query(query=delete_id_user.format('users', id_user))
                db.execute_query(query=delete_id_user.format('contas', id_user))
                db.execute_query(query=delete_id_user.format('dados_pessoais', id_user))
                print('Usuario Deletado com Sucesso !!!')
                return
        elif opt == 'N':
            print('Ok, Retornando para o Menu')
        else:
            print(error_option_invalid)
        print("\n")
        os.system("pause")
        return

    def show_requisitions(self):
        list_requisitions = db.read_query(query='SELECT * FROM operacoes '
                                                'WHERE tipo_operacao LIKE "%Requisicao%" AND aprovado LIKE "%NAO%"')
        list_requisitions = self.__tabulate_requisitons(list_requisitions=list_requisitions)
        headers = ["Id Da Operacao", "Tipo da Requisicao", "Valor Requisicao", "Data e Hora", "APROVADO", "Nome do Requisitor"]
        print(tabulate(list_requisitions, headers=headers))
        id_req_approved = int(input('\nEscolha o id da Requisicao que deseja aprovar (-1 P/ VOLTAR): '))
        if id_req_approved <= 0 or not (id_req_approved in [l[0] for l in list_requisitions]):
            print('Voltando ao Menu...')
        else:
            value_deposit = [l[2] for l in list_requisitions if l[0] == id_req_approved][0]
            print(value_deposit)
            id_account_req = db.read_query(query=f'SELECT id_conta_operada FROM operacoes WHERE id_operacao = {id_req_approved}')[0][0]
            id_user_approved = db.read_query(query=consult_id_user.format(id_account_req))[0][0]
            print(id_user_approved)
            db.update_column(table='operacoes', column='aprovado',
                             value='"SIM"', condition=f'id_operacao = {id_req_approved}')
            Client.update_balance(increment=float(value_deposit), sign='+', id_user=id_user_approved)
            print('Requisicao Aprovada !!!')
        os.system('pause')
        return

    @staticmethod
    def __tabulate_requisitons(list_requisitions):
        list_requisitions = [list(t) for t in list_requisitions]
        for req in list_requisitions:
            id_user = db.read_query(query=consult_id_user.format(req[2]))[0][0]
            name_req = db.read_query(query=consult_name.format(id_user))[0][0]
            del req[2]
            req[2] = float(req[2])
            req.append(name_req)
        return list_requisitions
