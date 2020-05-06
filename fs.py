# -*- coding: utf-8 -*-

import os
import click
from fstmt import TableAdaptorFactory, DashboardFactory, table

def get_data_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def get_database_path():
    return os.path.join(get_data_dir(), 'fstmt.sqlite')

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.argument('market')
@click.argument('symbol')
@click.option('--year', type=int)
@click.option('--quarter', type=int, default=4)
@click.option('--col', type=(str, int), multiple=True)
def insert(target, market, symbol, year, quarter, col):
    t = TableAdaptorFactory(get_database_path()).by_shortcut(target)
    market = market.upper()
    if isinstance(t, table.Stock):
        if year is not None:
            raise Exception("Providing 'year' when creating stocks")
        if col :
            raise Exception("Providing 'col' when creating stocks")
        t.insert(market, symbol)
    else:
        mul_by_1000 = ()
        for c in col:
            mul_by_1000 += ((c[0], c[1]*1000),)
        t.insert(market, symbol, year, quarter, mul_by_1000)

@cli.command()
@click.argument('target')
@click.argument('market')
@click.argument('symbol')
@click.option('--year')
@click.option('--quarter', type=int, default=4)
def delete(target, market, symbol, year, quarter):
    t = TableAdaptorFactory(get_database_path()).by_shortcut(target)
    market = market.upper()
    t.delete(market, symbol, year, quarter)

@cli.command()
@click.argument('target')
@click.argument('market')
@click.argument('symbol')
def query(target, market, symbol):
    d = DashboardFactory(get_database_path()).by_shortcut(target)
    market = market.upper()
    d.draw(market, symbol)

@cli.command()
@click.argument('target')
def migrate(target):
    t = TableAdaptorFactory(get_database_path()).by_shortcut(target)
    t.migrate()

if __name__ == '__main__':
    cli()
