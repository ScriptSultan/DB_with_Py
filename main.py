import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS name_bd (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phones INT NOT NULL
            );
            """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS phone_t (
                    phone_id SERIAL PRIMARY KEY,
                    number VARCHAR(20),
                    client_id int references clients(client_id)
                );
                """)
    return cur.fetchall()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO name_bd(first_name, last_name, email) VALUES(
                %s, %s, %s, %s);"""), (first_name, last_name, email, phones)
    return cur.fetchone()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO phone_t(number, client_id) VALUES(
                %s, %s)"""), (phone, client_id)
    return cur.fetchone()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE name_bd
                SET first_name=%s, last_name=%s, email=%s, phones=%s
                WHERE client_is=%s;
                """), (first_name, last_name, email, phones, client_id)
    return cur.fetchone()


def delete_phone(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE phone FROM phone_t
                WHERE client_id=%s
                """), (client_id)
    return cur.fetchone()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM name_bd
                WHERE client_id=%s
                """), (client_id)
    return


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT first_name, last_name, email, phone FROM name_bd
                WHERE first_name=%s AND last_name=%s AND email=%s AND phone=%s
                """), (first_name, last_name, email, phone)
    return cur.fetchone()


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    pass

conn.close()