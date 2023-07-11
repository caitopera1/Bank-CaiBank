import re
import datetime


menu_client = ("01 ------------------ SAQUE\n"
              "02 ------------------ DEPOSITO\n"
              "03 ------------------ TRANSFERENCIA\n"
              "04 ------------------ CONSULTAR SALDO\n"
              "05 ------------------ EXTRATO\n"
              "06 ------------------ MENU POUPANCA\n"
              "07 ------------------ MEUS DADOS\n"
              "08 ------------------ SAIR")


menu_adm = ("01 ------------------ VER REQUISIÇÕES DE OPERACOES\n"
            "02 ------------------ DELETAR CLIENTE\n"
            "03 ------------------ BLOQUEAR CONTA\n"
            "04 ------------------ SAIR\n")

menu_poupanca =  ("01 ------------------ DEPOSITO NA POUPANCA\n"
                  "02 ------------------ SAQUE P/ CONTA\n"
                  "03 ------------------ CONSULTAR SALDO POUPANCA\n"
                  "04 ------------------ VOLTAR")


error_option_invalid = ("ERROR : Opcao Invalida\n Tente Novamente (Aperte ENTER Para Continuar)")

limit_deposit = 1_000
limit_transfer = 1_000


def time_now():
    time_f = datetime.datetime.now()
    time_f = time_f.strftime('%Y-%m-%d %H:%M:%S')
    return time_f


def verify_unwritten(string):
    if string == '':
        return True
    return False

def verify_cpf(cpf):
    cpf_model = re.sub(r'\d', 'X', cpf)
    if cpf_model == "XXX.XXX.XXX-XX":
        return True
    return False
    
def verify_account_number(num_account):
    all_digits = re.findall("\d", num_account) 
    if len(all_digits) == 8 and len(num_account) == 8:
        return True
    return False

def verify_date_birth(date_birth):
    date_model = re.sub(r'\d', 'X', date_birth)
    if date_model == "XXXX-XX-XX":
        return True
    return False

def verify_number_value(number):
    if verify_unwritten(str(number)):
        return False
    return True
        

# Taxa por Hora
rate_poupanca = 0.5
