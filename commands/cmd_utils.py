import click
from click import Option, UsageError
from datetime import datetime
import os
from pathlib import Path

def log(msg: str, color: str, stderr: bool = False)-> None:
    click.echo(click.style(f'{datetime.now()} {msg}', color), err=stderr)

def create_directory(directory: str):
    homepath = os.path.expanduser("~")
    dir = os.path.join(homepath, directory)
    Path.mkdir(Path(dir), parents=True, exist_ok=True)


class MutuallyExclusiveOption(Option):
    """_Implements click mutally exclusive options_

    Args:
        Option (_click.option_): _Options(s) from click.option decorator_
    """
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ' [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "`{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

class RequiredIfOption(Option):
    """_Implements click requiredIf options_

    Args:
        Option (_click.option_): _Options(s) from click.option decorator_
    """
    def __init__(self, *args, **kwargs):
        self.required_if = set(kwargs.pop('required_if', []))
        help = kwargs.get('help', '')
        if self.required_if:
            ex_str = ', '.join(self.required_if)
            kwargs['help'] = help + (
                ' NOTE: This argument is required if '
                ' [' + ex_str + '].'
            )
        super(RequiredIfOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.required_if.intersection(opts) and self.name not in opts:
            raise UsageError(
                "Illegal usage: `{}` is required when "
                "`{}`.".format(
                    self.name,
                    ', '.join(self.required_if)
                )
            )

        return super(RequiredIfOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )