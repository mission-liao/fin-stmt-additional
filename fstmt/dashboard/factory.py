# -*- coding: utf-8 -*-

from ..table import TableAdaptorFactory

from .cost_analysis import CostAnalysis

class DashboardFactory:

    shortcut_mapping = {
        'ca': CostAnalysis
    }

    def __init__(self, db_path):
        self.db = TableAdaptorFactory(db_path)

    def by_shortcut(self, shortcut):
        t = DashboardFactory.shortcut_mapping.get(shortcut, None)
        if t is None:
            raise Exception('unknown shortcut: {}'.format(shortcut))
        return t(self.db)
