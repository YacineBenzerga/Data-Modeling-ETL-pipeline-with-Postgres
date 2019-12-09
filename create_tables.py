import psycopg2
from sql_queries import create_tbl_queries, drop_tbl_queries


def create_db(dbname):
    try:
        conn = psycopg2.connect("host=127.0.0.1")
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        # Drop & Create db
        cur.execute("DROP DATABASE IF EXISTS {}".format(dbname))
        cur.execute("CREATE DATABASE {}".format(dbname))
        # close default connection
        conn.close()
    except psycopg2.Error as e:
        print(e)


def init_db_conn(dbname):
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname={}".format(dbname))
        cur = conn.cursor()
        return cur, conn
    except psycopg2.Error as e:
        print(e)


def drop_tbles(cur, conn):
    try:
        for query in drop_tbl_queries:
            cur.execute(query)
            conn.commit()
    except psycopg2.Error as e:
        print("Error: Couldn't execute query")
        print(e)


def create_tbles(cur, conn):
    try:
        for query in create_tbl_queries:
            cur.execute(query)
            conn.commit()
    except psycopg2.Error as e:
        print("Error: Couldn't execute query")
        print(e)


def main():
    create_db("spokifydb")
    cur, conn = init_db_conn("spokifydb")

    drop_tbles(cur, conn)
    create_tbles(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
