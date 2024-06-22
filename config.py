SECRET_KEY = 'vds_gpcit'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}@{servidor}/{database}'.format(
      SGBD = 'mysql',
      usuario= 'root',
      servidor= 'localhost',
      database= 'vendas_gpc',
    )
