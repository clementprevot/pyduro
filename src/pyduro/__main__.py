#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------

import argparse
import json

from pyduro.actions import FUNCTIONS, STATUS_PARAMS, discover, get, set, raw

# --------------------------------------------------------------------------------------------------


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
        "-v",
        "--verbose",
        help="Display the raw frames sent and received",
        action="store_true",
    )

    # create sub-parser
    sub_parsers = parser.add_subparsers(title="Action", dest="action")

    sub_parsers.add_parser("discover", help="Discover any burner on your network")

    sub_parsers.add_parser("status", help="Get status of the burner")

    parser_get = sub_parsers.add_parser("get", help="Get information from a burner")
    parser_get.add_argument(
        "function_name",
        help="Specify the part of the burner you want to query",
        type=str,
        choices=FUNCTIONS,
    )
    parser_get.add_argument(
        "path",
        help="The path for your query",
        type=str,
        nargs="?",
    )

    parser_raw = sub_parsers.add_parser("raw", help="Send raw request to a burner")
    parser_raw.add_argument(
        "function_id",
        help="Specify the function you want to call on the burner",
        type=int,
    )
    parser_raw.add_argument(
        "payload",
        help="The payload of your request",
        type=str,
        nargs="?",
    )

    parser_set = sub_parsers.add_parser("set", help="Update setting of a burner")
    parser_set.add_argument(
        "path",
        help="The path for your modification",
        type=str,
    )
    parser_set.add_argument(
        "value",
        help="The payload for your modification",
        type=str,
    )

    args = parser.parse_args()

    response = None
    if args.action is None or args.action == "discover":
        response = discover.run(verbose=args.verbose)
    elif args.action == "status":
        response = raw.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            function_id=11,
            payload="*",
            verbose=args.verbose,
        )
    elif args.action == "get":
        response = get.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            function_name=args.function_name,
            path=args.path,
            verbose=args.verbose,
        )
    elif args.action == "raw":
        response = raw.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            function_id=args.function_id,
            payload=args.payload,
            verbose=args.verbose,
        )
    elif args.action == "set":
        response = set.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            path=args.path,
            value=args.value,
            verbose=args.verbose,
        )

    if response:
        if args.action == "status":
            status = response.parse_payload().split(",")
            i=0
            for key in STATUS_PARAMS:
                STATUS_PARAMS[key]=status[i]
                i+=1
            print(str(STATUS_PARAMS))
        elif args.action == "get":
            print(json.dumps(response.parse_payload(), sort_keys=True, indent=2))
        else:
            print(response.parse_payload())

        exit(response.status)

    exit(1)


# --------------------------------------------------------------------------------------------------

main()
