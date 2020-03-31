#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

import argparse
import importlib

from actions import ACTIONS

#-----------------------------------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Discover, query or modify an Aduro wood/pellet burner using the NBE communication protocol'
    )
    parser.add_argument(
        'action',
        help='run the given action (Default = "discover")',
        type=str,
        choices=ACTIONS,
        nargs='?',
        default=ACTIONS[0]
    )

    args = parser.parse_args()

    importlib.import_module(f'actions.{args.action}').run()

#-----------------------------------------------------------------------------------------------------------------------

main()
