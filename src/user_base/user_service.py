import psycopg2

def init():
    conn = psycopg2.connect(
        database="HakatonRisks",
        user='postgres',
        password='riski',
        host='localhost',
        port='5432'
    )
    print("соединение с базой прошло успешно")
    return conn

def get_user_info(fio, connection):
    cursor = connection.cursor()
    cursor.execute("""
                SELECT * 
                FROM user_info u
                WHERE u.fio = %s;
                """,
                [fio,]
            )
    sql_result = cursor.fetchone()
    print(type(sql_result))
    print(sql_result)
    cursor.close()
    return sql_result

