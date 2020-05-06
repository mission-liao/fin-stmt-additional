# -*- coding: utf-8 -*-

from collections import OrderedDict

class ProductCost:

    cols = {'product', 'capacity', 'volume', 'value'}

    def __init__(self, conn):
        self.conn = conn
        self.__prepare()

    def __prepare(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS product_cost (
            stock_market TEXT NOT NULL,
            stock_symbol TEXT NOT NULL,
            year         INTEGER NOT NULL,
            quarter      INTEGER NOT NULL,
            product      TEXT NOT NULL,
            capacity     INTEGER NOT NULL,
            volume       INTEGER NOT NULL,
            value        INTEGER NOT NULL,
            CONSTRAINT price_pk PRIMARY KEY (stock_market, stock_symbol, year, quarter, product),
            CONSTRAINT price_market_fk FOREIGN KEY (stock_market) REFERENCES stock(market),
            CONSTRAINT price_symbol_fk FOREIGN KEY (stock_symbol) REFERENCES stock(symbol)
        )
        ''')
        self.conn.commit()

    def insert(self, market, symbol, year, quarter, cols):
        data = dict()
        for c in cols:
            if c[0] not in ProductCost.cols:
                raise Exception('Unknown column for {}: {}'.format(ProductCost.__name__, c[0]))
            data[c[0]] = c[1]
        self.conn.execute('''
            INSERT INTO product_cost (
                stock_market,
                stock_symbol,
                year,
                quarter,
                product,
                capacity,
                volume,
                value)
            VALUES (?,?,?,?,?,?,?,?)''', (market, symbol, year, quarter,
                data['product'],
                data['capacity'],
                int(data['volume']),
                int(data['value'])*1000))
        self.conn.commit()

    def query(self, market, symbol, products):
        stmt = ''
        if len(products) > 0:
            stmt = '''
                SELECT
                    year, quarter, product, capacity, volume, value
                FROM
                    product_cost
                WHERE
                    stock_market=? AND stock_symbol=? AND product IN (?
            '''
            for p in products[1:]:
                stmt += ',?'
            stmt += ')'
        else:
            stmt = '''
                SELECT 
                    year, quarter, product, capacity, volume, value
                FROM
                    product_cost
                WHERE
                    stock_market=? AND stock_symbol=?
            '''
        stmt += ' ORDER BY year, product'
        c = self.conn.cursor()
        rows = []
        try:
            c.execute(stmt, (market, symbol)+products)
            rows = c.fetchall()
        finally:
            c.close()
        # cross-product of year, product.
        years, products = set(), set()
        for r in rows:
            years.add(r['year'])
            products.add(r['product'])
        od = OrderedDict()
        for y in sorted(list(years)):
            od[y] = OrderedDict()
            for p in sorted(list(products)):
                od[y][p] = (None, None, None)
        for r in rows:
            od[r['year']][r['product']] = (r['capacity'], r['volume'], r['value'])
        return od, products

