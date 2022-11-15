# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------
import time
from protocol import (
    FUNCTIONS,
    PAYLOADS,
    FunctionNotFoundException,
    PayloadToLargeException,
)
from protocol.frame import Frame

# -----------------------------------------------------------------------------------------------------------------------


def run(burner_address, serial, pin_code, function_name, path, value):
    """
    Get information from the given burner.

    Args:
        burner_address (str): The IP address of the burner.
        serial (str): The serial number of the burner (this can often be found on a sticker somewhere on the burner).
            Note that this should be a 6 characters string. Any longer string will be truncated and any shorter string
            will be left padded with 0s.
        pin_code (str): The secret pincode of the burner (this can often be found on a sticker somewhere on the burner).
            Note that this should be a 10 characters string. Any longer string will be truncated and any shorter string
            will be right padded with 0s.
        function (int): The part of the burner information you want to get.
        path (str): The path of the payload to modify on the burner.
        value (str): The new value to set the payload on the burner.
    """

    settings = (
        "boiler",
        "hot_water",
        "regulation",
        "weather",
        "weather2",
        "oxygen",
        "cleaning",
        "hopper",
        "fan",
        "auger",
        "ignition",
        "pump",
        "sun",
        "vacuum",
        "misc",
        "alarm",
        "manual",
    )

    try:
        function = FUNCTIONS.set.value

        if path is None or len(path) == 0:
            print("You must pass one of the following as path: {}".format(settings))

            return

        payload = "{}={}".format(path, value)

        frame = Frame(serial, pin_code, function, payload)

        response = frame.send(burner_address)

        return response
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
