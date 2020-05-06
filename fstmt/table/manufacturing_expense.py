# -*- coding: utf-8 -*-

class ManufacturingExpense:

    cols = {'薪資支出', '保險費', '修繕費', '水電費', '折舊', '燃料費', '包裝費', '環保支出', '其他費用', '雜費'}

    def __init__(self, conn):
        self.conn = conn
        self.__prepare()

    def __prepare(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS manufacturing_expense (
            stock_market   TEXT NOT NULL,
            stock_symbol   TEXT NOT NULL,
            year           INTEGER NOT NULL,
            quarter        INTEGER NOT NULL,
            薪資支出       INTEGER,
            保險費         INTEGER,
            修繕費         INTEGER,
            水電費         INTEGER,
            折舊           INTEGER,
            燃料費         INTEGER,
            包裝費         INTEGER,
            環保支出       INTEGER,
            其他費用       INTEGER,
            雜費           INTEGER,
            CONSTRAINT manufacturing_expense_pk PRIMARY KEY (stock_market, stock_symbol, year, quarter),
            CONSTRAINT manufacturing_expense_market_fk FOREIGN KEY (stock_market) REFERENCES stock(market),
            CONSTRAINT manufacturing_expense_symbol_fk FOREIGN KEY (stock_symbol) REFERENCES stock(symbol)
        )
        ''')
        self.conn.commit()

    def insert(self, market, symbol, year, quarter, cols):
        for c in cols:
            if c[0] not in ManufacturingExpense.cols:
                raise Exception('Unknown column: {}'.format(c[0]))
        params = (market, symbol, year, quarter)
        stmt = '''INSERT INTO manufacturing_expense (
            stock_market, 
            stock_symbol,
            year,
            quarter'''
        for c in cols:
            if stmt[-1] != ',':
                stmt += ','
            stmt += ' ' + c[0]
            params += (c[1],)
        stmt += ') VALUES ('
        for _ in range(len(params)-1):
            stmt += "?,"
        stmt += "?)"
        self.conn.execute(stmt, params)
        self.conn.commit()

    def query(self, market, symbol, cols):
        stmt = 'SELECT year,'
        for c in cols:
            if stmt[-1] != ',':
                stmt += ','
            stmt += c + ' '
        stmt += 'FROM manufacturing_expense WHERE stock_market=? AND stock_symbol=? ORDER BY year'
        c = self.conn.cursor()
        try:
            c.execute(stmt, (market, symbol))
            return c.fetchall()
        finally:
            c.close()

