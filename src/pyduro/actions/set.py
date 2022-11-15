# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------
from pyduro.actions import SETTINGS
from pyduro.protocol import (
    FUNCTIONS,
    FunctionNotFoundException,
    PayloadToLargeException,
)
from pyduro.protocol.frame import Frame

# -----------------------------------------------------------------------------------------------------------------------


def run(burner_address, serial, pin_code, path, value, verbose=False):
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
        path (str): The path of the payload to modify on the burner.
        value (str): The new value to set the payload on the burner.
        verbose (bool): Indicates if we want the frame to be printed before sending it.
            Default: False
    """

    try:
        function = FUNCTIONS.set.value

        if path is None or len(path) == 0:
            print("You must pass one of the following as path: {}".format(SETTINGS))

            return

        payload = "{}={}".format(path, value)

        frame = Frame(serial, pin_code, function, payload)

        response = frame.send(burner_address, verbose=verbose)

        return response
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
