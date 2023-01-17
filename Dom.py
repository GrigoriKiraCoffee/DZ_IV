import psycopg2

def create_db(cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) UNIQUE NOT NULL,
        last_name VARCHAR(100) UNIQUE NOT NULL,
        mailing_address TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS number_phone(
        number_phone_id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(client_d),
        number_phone VARCHAR(20) 
        );
    """)
def add_clients(conn, first_name, last_name, mailing_address, number_phone=None):
    cur.execute("""
        INSERT INTO clients(first_name, last_name, mailing_address)
        VALUES(%s, %s, %s, %s) RETURNING client_id;
        """, (first_name, last_name, mailing_address))
    client_id = cur.fetchone()
    cur.execute("""
        INSERT INTO number_phone(client_id, number_phone)
        VALUES(%s, %s);
        """, (client_id, number_phone))

def add_number_phone(conn, client_id, number_phone=None):
    cur.execute("""
        INSERT INTO number_phone(client_id, number_phone)
        VALUES(%s);
        """, (client_id, number_phone))

def apdate_clients(conn, client_id, first_name=None, last_name=None, mailing_address=None, number_phone=None):
    if first_name != None:
        cur.execute("""
            UPDATE clients SET first_name=%s
            WHERE client_id=%s;
            """, (first_name, client_id))
        conn.commit()

    if last_name != None:
        cur.execute("""
            UPDATE clients SET last_name=%s
            WHERE client_id=%s;
            """, (last_name, client_id))

    if mailing_address != None:
        cur.execute("""
            UPDATE clients SET mailing_address=%s
            WHERE client_id=%s;
            """, (mailing_address, client_id))

    if number_phone != None:
        cur.execute("""
            UPDATE clients SET number_phone=%s
            WHERE client_id=%s;
            """, (number_phone, client_id))

def del_number_phone(conn, client_id, number_phone):
    cur.execute("""
        DELETE FROM number_phone
        WHERE client_id=%s AND number_phone=%s;
        """, (client_id, number_phone,))

def del_client(conn, client_id):
    cur.execute("""
        DELETE FROM number_phone
        WHERE client_id=%s;
        """, (client_id,))

    cur.execute("""
        DELETE FROM clients
        WHERE client_id=%s;
        """, (client_id,))

def find_client(conn, first_name=None, last_name=None, mailing_address=None, number_phone=None):
    cur.execute("""
        SELECT first_name, last_name, mailing_address, number_phone FROM clients
        JOIN number_phone ON a.client_id = b.number_phone_id
        WHERE first_name=%s OR last_name=%s OR mailing_address=%s OR number_phone=%s;
        """, (first_name, last_name, mailing_address, number_phone))
    return cur.fetchall()

with psycopg2.connect(database="DZ_IV", user="postgres", password="QWERTY") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE number_phone;
            """)

        cur.execute("""
            DROP TABLE clients;
            """)

        create_db(cur)
        add_clients(conn, 'Иван', 'Простой', 'iv@mail.ru', '89181221173')
        add_clients(conn, 'Александр', 'Голова', 'AG@gmail.ru', '89614881524')
        add_clients(conn, 'Геннадий', 'Дружба', 'G_d@yandex.ru', '89283771526')
        add_number_phone(conn, 1, '89881561617')
        apdate_clients(conn, 1, 'Сергей', 'Распутин', '777@mail.ru', '')
        del_number_phone(conn, 2, '89614881524')
        del_client(conn, 3)
        print(find_client(conn, last_name='Распутин'))

conn.close()




