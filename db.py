import sqlite3
from sqlite3 import Error

def post_sql_query(sql_query):
    with sqlite3.connect('my.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        reg_date TEXT);'''
    post_sql_query(users_query)

def register_user(user, username, first_name, last_name):
    user_check_query = 'SELECT * FROM USERS WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = 'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
        post_sql_query(insert_to_db_query )

create_tables()  # вызываем функцию создания таблицы users


@bot.message_handler(commands=['start'])
def start(message):
    register_user(message.from_user.id, message.from_user.username,
                  message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.from_user.id, f'Welcome  {message.from_user.first_name}' )
