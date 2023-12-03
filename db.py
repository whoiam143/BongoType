import sqlite3 as sql


def create_bd():  # Функция для создания база данных
    with sql.connect("results.db") as con:
        cur = con.cursor()

        cur.execute(""" CREATE TABLE IF NOT EXISTS score(
            date  TEXT,
            time  TEXT,
            words INTEGER,
            wpm   INTEGER,
            text  TEXT);
            """)

        con.commit()


def add_result(date, time, words, wpm, text):  # Функция для добовления результатов
    with sql.connect("results.db") as bd:
        cr = bd.cursor()

    cr.execute("""INSERT INTO score VALUES (?, ?, ?, ?, ?)""",
               (date, time, words, wpm, text))

    bd.commit()


def results():  # Функция для получения списка результатов
    with sql.connect("results.db") as bd:
        cr = bd.cursor()

        res = cr.execute("""SELECT wpm FROM score""")
        lst_of_res = [list(i)[0] for i in res if type(list(i)[0]) is int]
        if len(lst_of_res) == 0:
            lst_of_res.append(0)

    return lst_of_res



