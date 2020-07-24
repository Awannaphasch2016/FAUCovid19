from typing import Optional
from typing import Tuple

import click

# @click.command()
# @click.option('--pos', nargs=2, type=click.FLOAT)
# def findme(pos: Tuple[Optional[str]]):
from mypy.checker import nothing


@click.command()
@click.option('--n', default=None)
# def dots(n: Optional[Tuple[str,...]]):
def dots(n):
    click.echo('.' * n)


if __name__ == '__main__':
    dots()

