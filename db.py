import sqlite3
DATABASE_URI = "db/leaderboard.db"

# Create a SQLite database if it doesn't exist already.


def create_tables():
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_scores (
        username TEXT,
        trick_score TEXT,
        treat_score INTEGER
    )
    ''')

    conn.commit()
    conn.close()


def add_user(username):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO player_scores (username, trick_score, treat_score) VALUES (?, 0, 0)", (username,))
    conn.commit()


def update_score(username, score_type):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    if score_type == "trick":
        cursor.execute(
            "UPDATE player_scores SET trick_score = trick_score + 1 WHERE username=?", (username,))
    if score_type == "treat":
        cursor.execute(
            'UPDATE player_scores SET treat_score = treat_score + 1 WHERE username=?', (username,))
    conn.commit()


def check_table(username):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player_scores WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    return existing_user


def get_score(username):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT trick_score, treat_score FROM player_scores WHERE username=?", (username,))
    res = cursor.fetchone()
    return res


create_tables()
