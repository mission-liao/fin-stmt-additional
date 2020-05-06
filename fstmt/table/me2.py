# -*- coding: utf-8 -*-

class ManufacturingExpense2:

    def __init__(self, conn):
        self.conn = conn
        self.__prepare()

    def __prepare(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS me2 (
            stock_market TEXT NOT NULL,
            stock_symbol TEXT NOT NULL,
            year         INTEGER NOT NULL,
            quarter      INTEGER NOT NULL,
            key          TEXT NOT NULL,
            value        INTEGER NOT NULL,
            CONSTRAINT manufacturing_expense_pk PRIMARY KEY (stock_market, stock_symbol, year, quarter, key),
            CONSTRAINT manufacturing_expense_market_fk FOREIGN KEY (stock_market) REFERENCES stock(market),
            CONSTRAINT manufacturing_expense_symbol_fk FOREIGN KEY (stock_symbol) REFERENCES stock(symbol)
        )
        ''')
        self.conn.commit()

    def insert(self, market, symbol, year, quarter, cols):
        pk = (market, symbol, year, quarter)
        stmt = '''INSERT INTO me2 (
            stock_market,
            stock_symbol,
            year,
            quarter,
            key,
            value)
        VALUES(?,?,?,?,?,?)'''
        for c in cols:
            self.conn.execute(stmt, pk+c)
        self.conn.commit()

    def query(self, market, symbol, cols):
        if len(cols) == 0:
            raise Exception('empty columns queried')
        stmt = '''
        SELECT
            year, key, value
        FROM
            me2
        WHERE
            stock_market=? AND stock_symbol=? AND quarter=? AND key IN (?'''
        for _ in cols[1:]:
            stmt += ',?'
        stmt += ')'
        c = self.conn.cursor()
        rows = []
        try:
            c.execute(stmt, (market, symbol, 4) + cols)
            rows = c.fetchall()
        finally:
            c.close()
        d = dict()
        years = set()
        for r in rows:
            years.add(r['year'])
            if r['year'] not in d:
                d[r['year']] = dict()
            d[r['year']][r['key']] = r['value']
        years = sorted(list(years))
        data = []
        for y in years:
            yd = d[y]
            dd = dict()
            dd['year'] = y
            for c in cols:
                dd[c] = yd.get(c, None)
            data.append(dd)
        return data

    def migrate(self):
        stmt = '''INSERT INTO me2 (
            stock_market,
            stock_symbol,
            year,
            quarter,
            key,
            value)
        VALUES(?,?,?,?,?,?)'''
        cols = [
            '薪資支出',
            '保險費',
            '修繕費',
            '水電費',
            '折舊',
            '燃料費',
            '包裝費',
            '環保支出',
            '其他費用',
            '雜費',
        ]
        crs = self.conn.cursor()
        try:
            crs.execute('''
            SELECT
                stock_market,
                stock_symbol,
                year,
                quarter,
                薪資支出,
                保險費,
                修繕費,
                水電費,
                折舊,
                燃料費,
                包裝費,
                環保支出,
                其他費用,
                雜費
            FROM
                manufacturing_expense''')
            rows = crs.fetchall()
            for r in rows:
                for c in cols:
                    if r[c] is None:
                        continue
                    crs.execute(stmt, (
                        r['stock_market'],
                        r['stock_symbol'],
                        r['year'],
                        r['quarter'],
                        c,
                        r[c],
                    ))
        finally:
            crs.close()
