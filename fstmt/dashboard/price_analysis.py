# -*- coding: utf-8 -*-

from terminaltables import AsciiTable
from colorclass import Color

class PriceAnalysis:

    def __init__(self, db):
        self.db = db

    def draw(self, market, symbol, args):
        products = ()
        for a in args:
            if a[0] == 'product':
                products += (a[1],)
            else:
                raise Exception('unknown args: {} for {}'.format(
                    a[0],
                    PriceAnalysis.__name__
                ))
        p_data, _, types = self.db.product_price().query(
            market, symbol, products
        )
        self._draw_price(p_data, types)
        c_data, _ = self.db.product_cost().query(
            market, symbol, products
        )
        self._draw_cost(c_data)

    def _draw_price(self, data, types):
        header = ('year', 'product')
        for t in types:
            header += (t + '-量', t + '-值', t + '-均價')
        header += ('總均價',)
        table_data = [header]
        for y, yd in data.items():
            for p, pd in yd.items():
                v = (y, p)
                vol, p = 0, 0
                for _, td in pd.items():
                    vol += td[0]
                    p += td[1]
                    v += (
                        td[0],
                        int(td[1]/1000),
                        "{:.2f}".format(td[1]/td[0] if td[0] else 0)
                    )
                v += ("{:.2f}".format(p/vol if p else 0),)
                table_data.append(v)
        table = AsciiTable(table_data)
        print(table.table)

    def _draw_cost(self, data):
        table_data = [('year', 'product', '產能', '產量', '產值', '利用率', '均成本')]
        for y, yd in data.items():
            for p, pd in yd.items():
                v = (y, p, pd[0], pd[1],
                    int(pd[2]/1000),
                    "{:03.2f}%".format(pd[1]*100/pd[0] if pd[0] else 0),
                    "{:.2f}".format(pd[2]/pd[1] if pd[1] else 0))
                table_data.append(v)
        table = AsciiTable(table_data)
        print(table.table)

