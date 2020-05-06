# -*- coding: utf-8 -*-

class Stock:

    def __init__(self, conn):
        self.conn = conn
        self.__prepare()

    def __prepare(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS stock (
            market TEXT NOT NULL,
            symbol TEXT NOT NULL,
            PRIMARY KEY (market, symbol)
        )
        ''')
        self.conn.commit()

    def insert(self, market, symbol):
        self.conn.execute(
            'INSERT INTO stock (market, symbol) VALUES(?, ?)',
            (market, symbol),
        )
        self.conn.commit()
