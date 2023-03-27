import sqlite3


def create_movie_table():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        movie_id INTEGER,
        UNIQUE(user_id, movie_id) ON CONFLICT REPLACE
    );
    ''')

    con.commit()
    con.close()


def add_movie_db(user, movie):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    cur.execute(f'''
        INSERT INTO movies(user_id, movie_id)
        VALUES ({user}, {movie});
    ''')

    con.commit()
    con.close()


def del_movie_db(user, movie):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    cur.execute(f'''
        DELETE FROM movies
        WHERE (user_id = {user}) AND (movie_id = {movie});
    ''')

    con.commit()
    con.close()


def get_all_user_movies_db(user):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    cur.execute(f'''
    SELECT movie_id
    FROM movies
    WHERE user_id = {user};
    ''')
    all_movies = cur.fetchall()

    con.close()
    return all_movies
