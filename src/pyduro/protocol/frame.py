# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------

import socket
from time import time

from pyduro.protocol import (
    DEFAULT_APP_ID,
    DEFAULT_LOCAL_ADDRESS,
    DEFAULT_NBE_PORT,
    DEFAULT_ORIGIN_PORT,
    END_CHAR,
    FUNCTIONS,
    MAX_PAYLOAD_SIZE,
    START_CHAR,
    FunctionNotFoundException,
    PayloadToLargeException,
    ResponseMalformedException,
)

# --------------------------------------------------------------------------------------------------


class Frame:
    """
    Defines a NBE communication to send request to the burner controller and receive a response.

    Args:
        serial (str): The serial number of the burner (this can often be found on a sticker somewhere on the burner).
            Note that this should be a 6 characters string. Any longer string will be truncated and any shorter string
            will be left padded with 0s.
        pin_code (str): The secret pincode of the burner (this can often be found on a sticker somewhere on the burner).
            Note that this should be a 10 characters string. Any longer string will be truncated and any shorter string
            will be right padded with 0s.
        function (int): The code of the function to run (0: discover, 1: get settings, ...).
            Note that this should be a number between 0 and 11.
            Also note that it will always be sent as a two character string ("00", "01", ..., "11").
        payload (str): The payload of the function.
            Note that you cannot send a request without a payload. This is considered illegal in the NBE communication
            protocol.
            Also note that you cannot send a payload larger than 495 bytes.
        app_id (str): The application identifier you want to give to the burner. This has no real use for Aduro's
            burners, so you can safely go with the default one.
            Note that this should be a 12 characters string. Any longer string will be truncated and any shorter string
            will be right padded with underscores.
            Default: ___pyduro___
        sequence_number (int): The number of the sequence. This will be used to check that the response matches the
            request. If none is given, this will always be 0 and you won't have any request/response matching check.
            Note that this will be a number modulo 99.
            Also note that it will always be sent as a two character string ("00", "01", ..., "99").
            Default: 0

    Attributes:
        app_id (str)
        function (int)
        payload (str)
        payload_size (int): The size of the payload.
        pin_code (str)
        sequence_number (int)
        serial (str)

    Throws:
        FunctionNotFoundException: If the given function is not allowed in the NBE protocol implemented by Aduro.
        PayloadToLargeException: If the given payload is larger than 495 bytes.
    """

    def __init__(
        self,
        serial,
        pin_code,
        function,
        payload,
        app_id=DEFAULT_APP_ID,
        sequence_number=0,
    ):
        self.app_id = "{:_<12.12}".format(app_id)
        self.serial = "{:0>6.6}".format(serial)
        self.pin_code = "{:0<10.10}".format(pin_code)
        self.function = function
        self.sequence_number = sequence_number % 99
        self.payload = payload if payload is not None else "*"
        self.payload_size = len(self.payload) if self.payload is not None else 0

        allowed_functions = set(function.value for function in FUNCTIONS)
        if self.function not in allowed_functions:
            raise FunctionNotFoundException(self.function)

        if self.payload_size > MAX_PAYLOAD_SIZE:
            raise PayloadToLargeException(self.payload)

    def get(self):
        """
        Returns the encoded NBE frame ready to be sent over to the burner via UDP.

        Returns:
            frame (str): The encoded NBE frame.
        """

        function = "{:02d}".format(self.function)
        sequence_number = "{:02d}".format(self.sequence_number)
        timestamp = "{:0>10.10}".format(str(time()))
        payload_size = "{:03d}".format(self.payload_size)

        frame = (
            f"{self.app_id}{self.serial} {START_CHAR}{function}{sequence_number}{self.pin_code}{timestamp}pad "
            f"{payload_size}{self.payload}{END_CHAR}"
        )

        return frame

    def send(
        self,
        destination_address,
        destination_port=DEFAULT_NBE_PORT,
        source_address=DEFAULT_LOCAL_ADDRESS,
        source_port=DEFAULT_ORIGIN_PORT,
        timeout=5,
        verbose=False,
    ):
        """
        Sends the frame to the burner over an UDP socket and wait for the response.

        Attributes:
            destination_addres (str): The ip address where to send the frame.
            destination_port (int): The port where to send the frame.
                Default: 8483 (default NBE communication protocol port)
            source_address (str): The ip address where to wait for a response.
                Default: 0.0.0.0 (any local IP)
            source_port (int): The local port where to wait for a response.
                Default: 1901 (port used by the Aduro Android application)
            timeout (int): The maximum duration to wait for a response from a burner, in seconds.
                If `None` is given, then the call will be blocking.
                Default: 5
            verbose (bool): Indicates if we want to display the frame before sending it.
                Default: False

        Returns:
            response (Response): The response from the burner (if any)
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((source_address, source_port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)

        if verbose:
            print(self.get().encode())

        sock.sendto(self.get().encode(), (destination_address, destination_port))

        try:
            response_frame, origin = sock.recvfrom(4096)

            if verbose:
                print(response_frame)

            return Response(response_frame.decode(), origin)
        except socket.timeout:
            print("No response received from a burner in less than 5 seconds!")
        except:
            print(
                "Unable to parse the answer from the burner ({}): {}".format(
                    origin, response_frame
                )
            )
            raise


class Response:
    """
    Defines a NBE communication received from a burner.

    Args:
        frame (Frame): The NBE frame received from the burner.
        origin (tuple(str, int)): The origin of the frame. The first item of the tuple is the ip address of the burner,
            the second one is the origin port.

    Attributes:
        app_id (str): The application identifier of the burner.
            Note that this will be a 12 characters string.
        burner_address (str): The ip address of the burner that sent the response.
        burner_port (int): The port the response of the burner came from.
        extra (str): The extra information the burner may add after the timestamp and before the payload size.
        frame (str): The original received NBE frame.
        function (int): The code of the function the response is for (0: discover, 1: get settings, ...).
            Note that this will be a number between 0 and 11.
            Also note that it will always be sent as a two character string ("00", "01", ..., "11").
        payload (str): The payload of the response.
        payload_size (int): The size of the payload.
        pin_code (str): The secret pincode of the burner.
            Note that this will be a 10 characters string.
        sequence_number (int): The number of the sequence. It should match the request's one.
            Note that this will be a number modulo 99.
            Also note that it will always be sent as a two character string ("00", "01", ..., "99").
        serial (str): The serial number of the burner.
            Note that this will be a 6 characters string that may be left padded with 0s.
        timestamp (int): The timestamp of the response.

    Throws:
        ResponseMalformedException: If the received response frame doesn't match the NBE protocol specifications.
    """

    def __init__(self, frame, origin):
        self.frame = frame

        self.burner_address = origin[0]
        self.burner_port = origin[1]

        start = 0
        end = start + 12
        self.app_id = frame[start:end]

        start = end
        end = start + 6
        self.serial = frame[start:end]

        start = end + 1
        end = start + 2
        self.function = int(frame[start:end])

        start = end
        end = start + 2
        self.sequence_number = int(frame[start:end])

        start = end
        end = start + 1
        self.status = int(frame[start:end])

        start = end
        end = start + 3
        self.payload_size = int(frame[start:end])

        start = end
        end = start + self.payload_size
        if end > len(frame):
            raise ResponseMalformedException(frame)
        else:
            self.payload = frame[start:end]

    def parse_payload(self):
        if ";" not in self.payload:
            return self.payload

        items = {} if "=" in self.payload else []
        for item in self.payload.split(";"):
            if "=" not in item:
                items.append(item)
            else:
                name, value = item.split("=")
                items[name] = value

        return items
