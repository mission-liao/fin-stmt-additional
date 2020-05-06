# -*- coding: utf-8 -*-

from ..table import TableAdaptorFactory

from .cost_analysis import CostAnalysis
from .price_analysis import PriceAnalysis

class DashboardFactory:

    shortcut_mapping = {
        'ca': CostAnalysis,
        'pa': PriceAnalysis,
    }

    def __init__(self, db_path):
        self.db = TableAdaptorFactory(db_path)

    def by_shortcut(self, shortcut):
        t = DashboardFactory.shortcut_mapping.get(shortcut, None)
        if t is None:
            raise Exception('unknown shortcut: {}'.format(shortcut))
        return t(self.db)
