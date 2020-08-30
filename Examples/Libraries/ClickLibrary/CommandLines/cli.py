from CommandLines.group1 import example_cli
from CommandLines.RunningConditionsCommand import running_condition_option
import click

@click.group()
def cli():
    pass

cli.add_command(example_cli)

# cli.add_command(running_condition_option)


if __name__ == '__main__':
    cli()
