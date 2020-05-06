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
@click.option('--col', type=(str, str), multiple=True)
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
        t.insert(market, symbol, year, quarter, col)

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
@click.option('--arg', type=(str, str), multiple=True) 
def query(target, market, symbol, arg):
    d = DashboardFactory(get_database_path()).by_shortcut(target)
    market = market.upper()
    d.draw(market, symbol, arg)

@cli.command()
@click.argument('target')
def migrate(target):
    t = TableAdaptorFactory(get_database_path()).by_shortcut(target)
    t.migrate()

if __name__ == '__main__':
    cli()
