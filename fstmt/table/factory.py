# -*- coding: utf-8 -*-

import sqlite3
from .cost_breakdown import CostBreakdown
from .stock import Stock
from .manufacturing_expense import ManufacturingExpense 
from .me2 import ManufacturingExpense2
from .product_price import ProductPrice
from .product_cost import ProductCost

class TableAdaptorFactory:

    shortcut_mapping = {
        's':  Stock,
        'cb': CostBreakdown,
        'me': ManufacturingExpense,
        'me2': ManufacturingExpense2,
        'pp': ProductPrice,
        'pc': ProductCost,
    }

    def __init__(self, db_path):
        if db_path is None:
            raise Exception("path to DB is not provided")
        self.conn = sqlite3.connect(db_path)
        self.conn.isolation_level = None
        self.conn.row_factory = sqlite3.Row

    def stock(self):
        return Stock(self.conn)

    def cost_breakdown(self):
        return CostBreakdown(self.conn)

    def manufacturing_expense(self):
        return ManufacturingExpense(self.conn)

    def manufacturing_expense2(self):
        return ManufacturingExpense2(self.conn)

    def product_price(self):
        return ProductPrice(self.conn)

    def product_cost(self):
        return ProductCost(self.conn)

    def by_shortcut(self, shortcut):
        t = TableAdaptorFactory.shortcut_mapping.get(shortcut, None)
        if t is None:
            raise Exception('unknown shortcut: {}'.format(shortcut))
        return t(self.conn)
