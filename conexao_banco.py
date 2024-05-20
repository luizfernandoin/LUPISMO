import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="lupismo",
        user='postgres',
        password='armandim2016')

# Abra um cursor para realizar operações de banco de dados
cur = conn.cursor()

# Execute um comando: isso cria uma nova tabela
cur.execute('DROP TABLE IF EXISTS User;')
cur.execute('CREATE TABLE User (id serial PRIMARY KEY,'
                                 'username varchar (50) NOT NULL)'
                                 )
conn.commit()

cur.close()
conn.close()