import click

@click.command()
def hello():
    click.echo('Ehllo World!')

@click.command()
def initdb():
    click.echo('Ehllo Initialized the database!')

@click.command()
def dropdb():
    click.echo('Dropped the database')

if __name__ == '__main__':
    hello()