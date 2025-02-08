import click
import os
import sys
import json

from click import Option, UsageError
from datetime import datetime
from pathlib import Path


def log(msg: str, color: str, stderr: bool = False) -> None:
    click.echo(click.style(f"{datetime.now()} {msg}", color), err=stderr)


def create_directory(directory: str) -> str:
    homepath = os.path.expanduser("~")
    dir: str = os.path.join(homepath, directory)
    Path.mkdir(Path(dir), parents=True, exist_ok=True)
    return dir


def read_config(path: str) -> dict | None:
    """_Read zcli.json and return it_

    Args:
        path (str): _The full path to the config file

    Returns:
        dict | None: _The configuration json object or None_
    """
    config = None

    if os.path.isfile(path):
        with open(path) as f:
            config = json.load(f)

    return config


def get_default_profile(config: dict, profile_type: str) -> str:
    """_Get the defaults for a profile type_

    Args:
        config (dict): _The configuration object (see command.cmd_utils(read_config)_
        profile_type (str): _The profile type to get the defaults for_

    Returns:
        str: _The name of the default profile_
    """
    value: str = ""
    if "defaults" in config:
        default = config["defaults"]
        for entry in default:
            if "profiles" in entry:
                profiles = entry["profiles"]
                for profile in profiles:
                    if profile_type in profile:
                        value = profile[profile_type]
    return value


def get_zcli_property(config: dict, prop_name: str) -> str:
    """_Get zcli properties_

    Args:
        config (dict): _The configuration object (see command.cmd_utils(read_config)_
        prop_name (str): _The zcli property to return_

    Returns:
        str: _The name of the default profile_
    """
    value: str = ""
    if "defaults" in config:
        default = config["defaults"]
        for entry in default:
            if "zcli" in entry:
                zcli_entry = entry["zcli"]
                if "properties" in zcli_entry:
                    zcli_props = zcli_entry["properties"]
                    if prop_name in zcli_props:
                        value = zcli_props[prop_name]

    return value


def get_profile_data(
    config: dict, profile_name: str, profile_type: str, key: str
) -> str:
    """_Get data from named profile_

    Args:
        config (dict): _The configuration object (see command.cmd_utils(read_config)_
        profile_name (str): _Name of profile_
        profile_type (str): _Profile type_
        key (str): _The key od the value you want to retrieve_

    Returns:
        str: _The requested value_
    """

    value = ""

    if "profiles" in config:
        profiles = config["profiles"]
        if profile_name in profiles:
            profile = profiles[profile_name]
            if "type" in profile and profile["type"] == profile_type:
                if "properties" in profile:
                    props = profile["properties"]
                    if key in props:
                        value = str(props[key])

    return value

def process_response(errors: dict, response: dict, process_text: bool = False) -> None:
    """
    Process the response from the API

    Args:
        errors: dict: The error dictionary
        response: dict: The response from the API
        process_text: bool: Process the

    Returns: 
        None
    """

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
        if process_text:
            response_dict = json.loads(response.text)
            sys.stderr.write(f"{response_dict["message"]}\n")
            for utility_details in response_dict["details"]:
                details = utility_details.split("\n")
                for detail in details:
                    sys.stderr.write(f"{detail}\n")

    if response.text != "":
        sys.stdout.write(f"{response.text}\n")


class MutuallyExclusiveOption(Option):
    """_Implements click mutally exclusive options_

    Args:
        Option (click.option): Options(s) from click.option decorator
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + (
                " NOTE: This argument is mutually exclusive with  [" + ex_str + "]."
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with `{}`.".format(
                    self.name, ", ".join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


class RequiredIfOption(Option):
    """_Implements click requiredIf options_

    Args:
        Option (_click.option_): _Options(s) from click.option decorator_
    """

    def __init__(self, *args, **kwargs):
        self.required_if = set(kwargs.pop("required_if", []))
        help = kwargs.get("help", "")
        if self.required_if:
            ex_str = ", ".join(self.required_if)
            kwargs["help"] = help + (
                " NOTE: This argument is required if  [" + ex_str + "]."
            )
        super(RequiredIfOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.required_if.intersection(opts) and self.name not in opts:
            raise UsageError(
                "Illegal usage: `{}` is required when `{}`.".format(
                    self.name, ", ".join(self.required_if)
                )
            )

        return super(RequiredIfOption, self).handle_parse_result(ctx, opts, args)
    
def fix_required(ctx, param, value):
    if value == 'set':
        ctx.command.params[3].required = True
