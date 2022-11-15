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


def run(burner_address, serial, pin_code, function_name, path="*", verbose=False):
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
        function_name (str): The name of the function you want to run.
        path (str): The path of the payload to load from the burner (or the payload).
        verbose (bool): Indicates if we want the frame to be printed before sending it.
            Default: False
    """

    try:
        function_id = None

        if function_name == "settings":
            function_id = FUNCTIONS.get_settings.value

            if path is None or len(path) == 0:
                print("You must pass one of the following as path: {}".format(SETTINGS))

                return
        if function_name == "range":
            function_id = FUNCTIONS.get_settings_range.value
        elif function_name == "operating":
            function_id = FUNCTIONS.get_operating_data.value
        elif function_name == "advanced":
            function_id = FUNCTIONS.get_advanced_data.value
        elif function_name == "consumption":
            function_id = FUNCTIONS.get_consumption_data.value

            if path is None or len(path) == 0 or path not in CONSUMPTION_DATA:
                print(
                    "You must pass one of the following as path: {}".format(
                        CONSUMPTION_DATA
                    )
                )

                return
        elif function_name == "chart":
            function_id = FUNCTIONS.get_chart_data.value
        elif function_name == "logs":
            function_id = FUNCTIONS.get_event_log.value

            path = (
                time.strftime("%y%m%d:%H%M%S;", time.localtime())
                if path is None or len(path) == 0 or path == "now"
                else path
            )
        elif function_name == "info":
            function_id = FUNCTIONS.get_info.value
        elif function_name == "versions":
            function_id = FUNCTIONS.get_sw_versions.value

        frame = Frame(serial, pin_code, function_id, path)

        response = frame.send(burner_address, verbose=verbose)

        return response
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
