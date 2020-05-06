# -*- coding: utf-8 -*-

class CostBreakdown:

    cols = {'期初原料', '期末原料', '耗用原料', '期初物料', '期末物料', '耗用物料', '直接人工', '製造費用', '製造成本', '銷貨成本'}

    def __init__(self, conn):
        self.conn = conn
        self.__prepare()

    def __prepare(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS cost_breakdown (
            stock_market   TEXT NOT NULL,
            stock_symbol   TEXT NOT NULL,
            year           INTEGER NOT NULL,
            quarter        INTEGER NOT NULL,
            期初原料       INTEGER,
            期末原料       INTEGER,
            耗用原料       INTEGER,
            期初物料       INTEGER,
            期末物料       INTEGER,
            耗用物料       INTEGER,
            直接人工       INTEGER,
            製造費用       INTEGER,
            製造成本       INTEGER,
            銷貨成本       INTEGER,
            CONSTRAINT cost_breakdown_pk PRIMARY KEY (stock_market, stock_symbol, year, quarter),
            CONSTRAINT cost_breakdown_market_fk FOREIGN KEY (stock_market) REFERENCES stock(market),
            CONSTRAINT cost_breakdown_symbol_fk FOREIGN KEY (stock_symbol) REFERENCES stock(symbol)
        )''')
        self.conn.commit()

    def insert(self, market, symbol, year, quarter, cols):
        for c in cols:
            if c[0] not in CostBreakdown.cols:
                raise Exception('Unknown column: {}'.format(c[0]))
        params = (market, symbol, year, quarter)
        stmt = '''INSERT INTO cost_breakdown (
            stock_market, 
            stock_symbol,
            year,
            quarter'''
        for c in cols:
            if stmt[-1] != ',':
                stmt += ','
            stmt += ' ' + c[0]
            params += (int(c[1])*1000,)
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
        stmt += 'FROM cost_breakdown WHERE stock_market=? AND stock_symbol=? ORDER BY year'
        c = self.conn.cursor()
        try:
            c.execute(stmt, (market, symbol))
            return c.fetchall()
        finally:
            c.close()

    def delete(self, market, symbol, year, quarter):
        stmt = 'DELETE FROM cost_breakdown WHERE stock_market=? AND stock_symbol=? AND year=? AND quarter=?'
        self.conn.execute(stmt, (market, symbol, year, quarter))
        self.conn.commit()
