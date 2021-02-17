#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains custom click.command."""
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import cast

import click  # type: ignore

T = TypeVar('T', bound=Callable[..., Any])

def enfore_dependency_between_date_cli_args() -> T:
    """

    Enforce dependency between max_after and after_date&before_date.

    :rtype: CommandOptionRequiredClawis
    :return: a child class of click.Command with overriden function
    """
    required_date_options = ["max_after", ("before_date", "after_date")]

    class CommandOptionRequiredClass(click.Command):
        def invoke(self, ctx: click.Context):
            count = 0
            if ctx.params[required_date_options[0]] is not None:
                count += 2
            for i in required_date_options[1]:
                if ctx.params[i] is not None:
                    count += 1
            if count > 2:
                raise click.ClickException(
                    "if max_after is used, either before_date or after_date "
                    "cannot be used. Vice versa.",
                )
            super(CommandOptionRequiredClass, self).invoke(ctx)

    return cast(T, CommandOptionRequiredClass)
