# -*- coding: utf-8 -*-

from terminaltables import AsciiTable
from colorclass import Color

class CostAnalysis:

    def __init__(self, db):
        self.db = db

    def draw(self, market, symbol):
        cb_cols = (
            '耗用原料',
            '耗用物料',
            '直接人工',
            '製造費用',
            '製造成本',
            '銷貨成本',
        )
        cb_data = self.db.cost_breakdown().query(
            market, symbol, cb_cols,
        )
        me_cols = (
            '薪資支出',
            '保險費',
            '修繕費',
            '水電費',
            '折舊',
            '燃料費',
            '包裝費',
            '其他費用',
        )
        me_data = self.db.manufacturing_expense2().query(
            market, symbol, me_cols,
        )
        data = dict()
        for d in cb_data:
            v = []
            for c in cb_cols:
                v.append(d[c])
            data[d['year']] = v
        for d in me_data:
            if d['year'] not in data:
                data[d['year']] = ('?', '?', '?', '?', '?', '?')
            v = []
            for c in me_cols:
                v.append(d[c])
            data[d['year']] += v 
        # Arrange them for terminaltables.
        table_data = [('year',) + cb_cols + me_cols]
        for year in sorted(data.keys()):
            dd = data[year]
            if len(dd) == 6:
                dd += (None,)*8
            row1 = (year,)
            for d in dd:
                row1 += (int(d/1000),) if d is not None else (' ',)
            table_data.append(row1)
            row2 = (' ',)
            for d in dd[:6]:
                t = "{:03.2f}%".format(d/dd[4]*100) if d is not None else ' '
                row2 += (Color("{autogreen}" + t + "{/autogreen}"),)
            for d in dd[6:]:
                t = "{:03.2f}%".format(d/dd[3]*100) if d is not None else ' '
                row2 += (Color("{autogreen}" + t + "{/autogreen}"),)
            table_data.append(row2)
        table = AsciiTable(table_data)
        print(table.table)
