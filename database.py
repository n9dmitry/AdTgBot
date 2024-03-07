import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


def connection_data(*args):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS data
                          (id INTEGER PRIMARY KEY,
                          new_id TEXT,
                          date TEXT,
                          telegram TEXT)''')

        cursor.execute(
            "INSERT INTO data (new_id, date, telegram) VALUES (?, ?, ?, ?)",
            (new_id, date, telegram))

        conn.commit()
        # Выполняем запрос к базе данных
        cursor.execute("SELECT * FROM users")
        # Получаем результаты запроса
        rows = cursor.fetchall()
        # Выводим результаты
        for row in rows:
            print(row)
        conn.close()

    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)
    finally:
        conn.close()


seller_telegram = "@example_seller"
new_id = 12345
save_data(new_id, date, telegram)


# import traceback
# from functools import wraps
# # from e2e.conf import config
#
#
# def cursorize():
#     """Wrap function to setup and tear down a Postgres connection while
#     providing a cursor object to make queries with.
#     """
#
#     def wrap(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             return_val = None
#             try:
#                 # Setup postgres connection
    #                 conn = sqlite3.connect('database.db')
    #
    #                 cursor = conn.cursor()
    #                 # Call function passing in cursor
    #                 return_val = f(cursor, *args, **kwargs)
    #             except Exception as ex:
    #                 print('EX:', ex)
    #                 traceback.print_tb(ex.__traceback__)
    #             finally:
    #                 # Close connection
    #                 conn.commit()
    #                 conn.close()
    #             # print(f'{f.__name__} failed with kwargs {kwargs}')
    #             return return_val
    #
    #         return wrapper
    #
    #     return wrap