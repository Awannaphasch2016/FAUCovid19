import click
import os, sys

from src.Utilities import my_timer


@click.command()
@click.option('--with_tag/--no-with-tag',default=False)
@click.argument('first_argument') #str
# @click.argument('second_argument') #int
# @click.argument('thrid_arguemnt') #boolean
@click.pass_context
@my_timer
def first(ctx, with_tag, first_argument):
    print('with_tag = %s' % (with_tag and 'True' or 'False'))
    print(f'first_argument = {first_argument}')
    return ctx, with_tag, first_argument

# @click.command()
# @click.argument('second_argument')
# @click.pass_context
# def second(ctx, second_argument):
#     print(f'second_argument = {second_argument}')

# first.add_command(second)

if __name__ == '__main__':
    first(obj={})

