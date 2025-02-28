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

def get_user_info(fio, connection) -> str:
    cursor = connection.cursor()
    cursor.execute("""
                SELECT * 
                FROM user_info u
                WHERE u.fio = \'ДУМА АНАСТАСИЯ АЛЕКСАНДРОВНА\';
                """,
                [fio,]
            )
    sql_result = cursor.fetchone()
    result = ""
    for i in range(1, sql_result):
        result += str(sql_result[i]) + " "
    cursor.close()
    return result

