import click


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.pass_context
def sync(ctx):
    click.echo("Debug mode is %s" % (ctx.obj["DEBUG"] and "yes" or "no"))


if __name__ == "__main__":
    cli(obj={})
