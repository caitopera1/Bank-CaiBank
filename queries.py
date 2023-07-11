search_id_with_email = 'SELECT id_user FROM users WHERE users.email= "{}"'


select_join_userdata = 'SELECT u.id_user, u.email, u.password, u.ultimo_horario_entrada, ' \
                       'd.cpf, d.nome_completo, d.data_nascimento ' \
                       'FROM users AS u ' \
                       'INNER JOIN dados_pessoais AS d ' \
                       'ON u.id_user = d.id_user AND u.id_user = {}'

read_columns = 'SHOW COLUMNS FROM {}'

read_balance = 'SELECT saldo FROM contas WHERE id_user = {}'

read_balance_p = 'SELECT saldo FROM poupancas WHERE id_conta = {}'

create_operation = 'INSERT INTO operacoes (tipo_operacao, id_conta_operada, data_hora_operacao, valor_operacao, aprovado)' \
                   'VALUES ("{}", {}, "{}", {}, "{}")'

create_transfer = 'INSERT INTO transferencias (id_conta_beneficiario, id_conta_emissor, id_operacao)' \
                  'VALUES ({}, {}, {})'

consult_id_account = 'SELECT id_conta FROM contas WHERE id_user = {}'

read_operations = 'SELECT tipo_operacao, valor_operacao, data_hora_operacao, aprovado FROM operacoes ' \
                  'WHERE id_conta_operada = {}'

delete_id_user = 'DELETE FROM {} WHERE id_user = {};'

delete_id_account = 'DELETE FROM {} WHERE id_account = {}'

consult_id_user = 'SELECT id_user FROM contas WHERE id_conta = {}'

consult_name = 'SELECT nome_completo FROM dados_pessoais WHERE id_user = {}'

