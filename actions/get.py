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


def run(burner_address, serial, pin_code, function_name, path="*", value=None):
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
        value (str): Not used here.
    """

    root = (
        "settings",
        "operating_data",
        "advanced_data",
        "consumption_data",
        "event_log",
        "sw_versions",
        "info",
    )
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
    consumption_data = (
        "total_hours",
        "total_days",
        "total_months",
        "total_years",
        "dhw_hours",
        "dhw_days",
        "dhw_months",
        "dhw_years",
        "counter",
    )

    try:
        function = None

        if function_name == "settings":
            function = FUNCTIONS.get_settings.value

            if path is None or len(path) == 0:
                print("You must pass one of the following as path: {}".format(settings))

                return
        if function_name == "range":
            function = FUNCTIONS.get_settings_range.value
        elif function_name == "operating":
            function = FUNCTIONS.get_operating_data.value
        elif function_name == "advanced":
            function = FUNCTIONS.get_advanced_data.value
        elif function_name == "consumption":
            function = FUNCTIONS.get_consumption_data.value

            if path is None or len(path) == 0 or path not in consumption_data:
                print(
                    "You must pass one of the following as path: {}".format(
                        consumption_data
                    )
                )

                return
        elif function_name == "chart":
            function = FUNCTIONS.get_chart_data.value
        elif function_name == "logs":
            function = FUNCTIONS.get_event_log.value

            path = (
                time.strftime("%y%m%d:%H%M%S;", time.localtime())
                if path is None or len(path) == 0 or path == "now"
                else path
            )
        elif function_name == "info":
            function = FUNCTIONS.get_info.value
        elif function_name == "versions":
            function = FUNCTIONS.get_sw_versions.value

        frame = Frame(serial, pin_code, function, path)

        response = frame.send(burner_address)

        return response
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
