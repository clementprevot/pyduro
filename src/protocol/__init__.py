# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------

import enum

# -----------------------------------------------------------------------------------------------------------------------

DEFAULT_APP_ID = "___pyduro___"

DEFAULT_NBE_PORT = 8483
DEFAULT_ORIGIN_PORT = 1901
DEFAULT_LOCAL_ADDRESS = "0.0.0.0"


class PAYLOADS(enum.Enum):
    discovery = "NBE Discovery"


class FUNCTIONS(enum.Enum):
    discover = 0
    get_settings = 1
    get_settings_range = 3
    get_operating_data = 4
    get_advanced_data = 5
    get_consumption_data = 6
    get_chart_data = 7
    get_event_log = 8
    get_info = 9
    get_sw_versions = 10
    set = 2


START_CHAR = chr(0x02)
END_CHAR = chr(0x04)

MAX_PAYLOAD_SIZE = 495

# -----------------------------------------------------------------------------------------------------------------------


class FunctionNotFoundException(Exception):
    """
    Raised when the a function of a NBE frame request is not valid.
    """

    def __init__(self, function):
        self.message = f'The function "{function}" is not valid!'


class ResponseMalformedException(Exception):
    """
    Raised when the a frame received from a burner doesn't match the NBE protocol specifications.
    """

    def __init__(self, frame):
        self.message = f'The received frame ("{frame}") is malformed!'


class PayloadToLargeException(Exception):
    """
    Raised when the payload of a NBE frame request is larger than 495 bytes.
    """

    def __init__(self, payload):
        self.message = (
            f'The payload "{payload}" exceeds the maximum allowed payload size for a NBE frame'
            f"(size = {len(payload)}, max = {MAX_PAYLOAD_SIZE})!"
        )
