import sqlite3 as sql3


def db_conn():
    conn = sql3.connect('instance/masutier.db')
    conn.row_factory = sql3.Row
    return conn


def db_inject(sqlquery):
    conn = db_conn()
    conn.execute(sqlquery)
    conn.commit()
    conn.close()


def updateInforme(sqlQuery):
    conn = sql3.connect('instance/masutier.db')
    cur = conn.cursor()
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()


def checkDb(sqlquery):
    try:
        conn = db_conn()
        users = conn.execute(sqlquery).fetchone()
        conn.close()
    except:
        sqlQuery = """ CREATE TABLE users (firstName, lastName, email, phone, addres, state, contry, passwordHash)"""
        conn = db_conn()
        conn.execute(sqlQuery)
        conn.close()
        users = []
    return users


def askOne(sqlquery):
    try:
        conn = db_conn()
        users = conn.execute(sqlquery).fetchone()
        conn.close()
    except:
        users = []
    return users

