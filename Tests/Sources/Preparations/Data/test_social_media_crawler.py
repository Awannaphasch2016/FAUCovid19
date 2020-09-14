import pytest


# @pytest.mark.unit
# def test_main(input1, input2):
#     def _check_main_arg_condition(_max_after,
#                                   _before_date,
#                                   _after_date):
#         pass
#     _check_main_arg_condition(max_after, before_date, after_date)


from click.testing import CliRunner


import click
import sys


@click.command()
@click.option("--opt")
@click.argument("arg")
def hello(arg, opt):
    """A Simple program"""
    click.echo("Opt: {}  Arg: {}".format(opt, arg))


def test_hello_world():

    runner = CliRunner()
    result = runner.invoke(hello, ["--opt", "An Option", "An Arg"])
    assert result.exit_code == 0
    assert result.output == "Opt: An Option  Arg: An Arg\n"

    result = runner.invoke(hello, ["An Arg"])
    assert result.exit_code == 0
    assert result.output == "Opt: None  Arg: An Arg\n"


if __name__ == "__main__":
    # hello(sys.argv[1:])
    test_hello_world()
