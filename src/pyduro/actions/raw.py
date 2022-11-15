# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------
import time

from pyduro.actions import CONSUMPTION_DATA, SETTINGS
from pyduro.protocol import (
    FUNCTIONS,
    FunctionNotFoundException,
    PayloadToLargeException,
)
from pyduro.protocol.frame import Frame

# --------------------------------------------------------------------------------------------------


def run(burner_address, serial, pin_code, function_id, payload, verbose=False):
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
        function_id (int): The raw identifier of the function you want to run on the burner.
        payload (str): The payload to send to the burner.
        verbose (bool): Indicates if we want the frame to be printed before sending it.
            Default: False
    """

    try:
        frame = Frame(serial, pin_code, function_id, payload, function_check=False)

        response = frame.send(burner_address, verbose=verbose)

        return response
    except PayloadToLargeException as e:
        print(e.message)
