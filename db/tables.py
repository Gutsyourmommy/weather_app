from db.base import connect_db, commit_and_close


def create_users_table():
    conn, cursor = connect_db('../weather.db')
    sql = '''
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT
            
        );
    '''
    cursor.executescript(sql)

    commit_and_close(conn)


def create_weather_table():
    conn, cursor = connect_db('../weather.db')
    sql = '''
        DROP TABLE IF EXISTS weather;
        CREATE TABLE IF NOT EXISTS weather(
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT ,
            tz INTEGER,
            sunrise DATETIME,
            sunset DATETIME,
            dt DATERTIME,
            description TEXT,
            speed DECIMAL,
            temp DECIMAL,
            
            user_id INTEGER REFERENCES users(user_id)  
        );        
    '''
    cursor.executescript(sql)
    commit_and_close(conn)


# create_weather_table()
# create_users_table()























































