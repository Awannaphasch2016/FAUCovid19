import click


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
def sync():
    click.echo('Synching')

if __name__ == '__main__':
    cli()