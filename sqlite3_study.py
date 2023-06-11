import random
import sqlite3
import hashlib


# with sqlite3.connect("database.db") as db:  # automatically commit and close
#     cursor = db.cursor()

# cursor.execute(
#     """CREATE TABLE articles(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         author VARCHAR,
#         topic VARCHAR,
#         content TEXT)"""
# )
#
# values = [
#     ("Main", "About tomorrow", "All will be good"),
#     ("Red", "About today", "All will be good"),
#     ("Colt", "The advice of day", "Think about good news"),
# ]

# cursor.executemany(
#     "INSERT INTO articles(author, topic, content) VALUES(?, ?, ?)", values
# )


# cursor.execute("SELECT * FROM articles")
# print(cursor.fetchone())  # cursor.__next__()
# print(cursor.fetchmany(1))
# print(cursor.fetchall())
# cursor.execute(
#     """CREATE TABLE email(`from` VARCHAR, subject VARCHAR, content TEXT)"""  # use `` because from is keyword
# )
# cursor.execute("INSERT INTO email VALUES('Well', 'Good day', 'All right' )")
# cursor.execute("SELECT `from` FROM email")
# print(cursor.fetchone()[0])
# --------------------------------------------------------------------------------------------------------
# db = sqlite3.connect("database.db")  # better to use block `with`.It does not need close & commit
# cursor = db.cursor()
# cursor.close()
# db.close()
# -------------------------------------------------------------------------------------------------------
def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()


with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        age INTEGER(3),
        sex INTEGER NOT NULL DEFAULT 1,
        balance INTEGER NOT NULL DEFAULT 2000,
        login VARCHAR(15),
        password VARCHAR(20)
    );
    CREATE TABLE IF NOT EXISTS casino(
    name VARCHAR(50),
    description TEXT(300),
    balance BIGINT NOT NULL DEFAULT 10000
    )
    """
    cursor.executescript(query)


def registration():
    name = input("Name: ")
    age = int(input("Age: "))
    sex = int(input("Sex: "))
    login = input("Login: ")
    password = input("Password: ")
    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        db.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        if cursor.fetchone() is None:
            values = [name, age, sex, login, password]
            cursor.execute(
                "INSERT INTO users(name, age, sex, login, password) VALUES(?, ?, ?, ?, md5(?))",
                values,
            )
            db.commit()
        else:
            print("Users exists")
            registration()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


def log_in():
    login = input("Login: ")
    password = input("Password: ")

    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        db.create_function("md5", 1, md5sum)

        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        if cursor.fetchone() is None:
            print("User with this login does not exists")
        else:
            cursor.execute(
                "SELECT password FROM users WHERE login = ? AND password = md5(?)",
                (login, password),
            )
            if cursor.fetchone() is None:
                print("Incorrect password")
            else:
                play_casino(login)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


def play_casino(login):
    print("\nCasino")

    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        cursor.execute(
            "SELECT age FROM users WHERE login = ? AND  age >= ?", (login, 18)
        )
        if cursor.fetchone() is None:
            print("You are too young")
        else:
            bet = int(input("Bet: "))
            number = random.randint(1, 100)

            balance = cursor.execute(
                "SELECT balance FROM users WHERE login = ?", (login,)
            ).fetchone()[0]
            if balance < bet:
                print("You don't have enough money")
            elif balance <= 0:
                print("You don't have enough money")
            else:
                if number < 50:
                    cursor.execute(
                        "UPDATE users SET balance = balance - ? WHERE login = ?",
                        (bet, login),
                    )
                    cursor.execute("UPDATE casino SET balance = balance + ?", (bet,))
                    print("You lose")
                else:
                    cursor.execute(
                        "UPDATE users SET balance = balance + ? WHERE login = ?",
                        (bet, login),
                    )
                    cursor.execute("UPDATE casino SET balance = balance - ?", (bet,))
                    print("You win")
                db.commit()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


registration()
log_in()
