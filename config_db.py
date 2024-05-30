import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `vendas_gpc`;")

cursor.execute("CREATE DATABASE `vendas_gpc`;")

cursor.execute("USE `vendas_gpc`;")

# criando tabelas
TABLES = {}
TABLES['Vendas'] = ('''
      CREATE TABLE `vendas` (
      `nf` int(11) NOT NULL,
      `data` text NOT NULL,
      `empresa` int(11) NOT NULL,
      `vendedor` varchar(40) NOT NULL,
      `cliente` varchar(150) NOT NULL,
      `produto` varchar(200) NOT NULL,
      `estado` varchar(20) NOT NULL,
      `valor` float NOT NULL,
      `valor_final` float NOT NULL,
      `parceiro` varchar(40) NOT NULL,
      PRIMARY KEY (`nf`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(50) NOT NULL,
      `nome_de_usuario` varchar(20) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nome_de_usuario`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nome_de_usuario, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Divino", "BD", "alohomora"),
      ("Camila Ferreira", "Mila", "paozinho"),
      ("Guilherme Louro", "Cake", "python_eh_vida")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from vendas_gpc.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo vendass
vendas_sql = 'INSERT INTO vendas (nf, data, empresa, vendedor, cliente, produto, estado, valor, valor_final, parceiro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
vendas = [
      (1418, '06/05/2024', 6, 'Fabricio', 'MT4 TECNOLOGIA', 'Processador', 'SP', 3980.00, 3980.00, "--"),
      (1394, '02/05/2024', 6, 'Fabricio', 'FUNDAÇÃO DE DESENVOLVIMENTO', 'HD', 'SP', 47520.00, 47520.00, '--'),
]
cursor.executemany(vendas_sql, vendas)

cursor.execute('select * from vendas_gpc.vendas')
print(' -------------  Vendas:  -------------')
for venda in cursor.fetchall():
    print(venda[4])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()