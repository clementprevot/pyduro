#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------

import argparse
import importlib

from actions import ACTIONS, FUNCTIONS

# -----------------------------------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        prog="PyDuro",
        description="Discover, query or modify an Aduro wood/pellet burner using the NBE communication protocol",
    )
    parser.add_argument(
        "-b",
        "--burner",
        help="The IP address of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--serial",
        help="The serial number of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--pin",
        help="The pin code of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "action",
        help='Run the given action (Default = "discover")',
        type=str,
        choices=ACTIONS,
        nargs="?",
        default=ACTIONS[0],
    )
    parser.add_argument(
        "function",
        help="Specify the part of the burner you want to query/modify",
        type=str,
        choices=FUNCTIONS,
        nargs="?",
    )
    parser.add_argument(
        "path",
        help="The path for your query/modification",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "value",
        help="The payload for your modification",
        type=str,
        nargs="?",
    )

    args = parser.parse_args()

    if args.action == "discover":
        importlib.import_module(f"actions.{args.action}").run()
    else:
        importlib.import_module(f"actions.{args.action}").run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            function_name=args.function,
            path=args.path,
            value=args.value,
        )


# -----------------------------------------------------------------------------------------------------------------------

main()
