import psycopg2

conn = None

try:
    conn = psycopg2.connect(
        database="mydb",
        host="localhost",
        user="postgres",
        password="password"
    )
    print("database ok")

finally:
    print("nz dali e ok")


cur = conn.cursor()

cur.execute('SELECT * FROM myschema.tabela')
for data in cur:
    print(data)

conn.close()
