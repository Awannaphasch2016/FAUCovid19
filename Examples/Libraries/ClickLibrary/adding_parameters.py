import click


@click.command()
@click.option("--count", default=1, help="number of greeting")
@click.argument("name")
def hello(count, name):
    for x in range(count):
        click.echo("Hello %s!" % name)


if __name__ == "__main__":
    hello()
