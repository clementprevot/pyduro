# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------

from pyduro.actions import DEFAULT_DISCOVERY_ADDRESS
from pyduro.protocol import (
    FUNCTIONS,
    PAYLOADS,
    FunctionNotFoundException,
    PayloadToLargeException,
)
from pyduro.protocol.frame import Frame

# --------------------------------------------------------------------------------------------------


def run(verbose=False):
    """
    Run the discovery of burner(s) in the local network.
    This trigger a specific "Discovery" frame on an UDP broadcat and wait for any burner(s) to send back a response

    Args:
        verbose (bool): Indicates if we want the frame to be printed before sending it.
            Default: False
    """

    try:
        frame = Frame(
            "<serial>", "<pin>", FUNCTIONS.discover.value, PAYLOADS.discovery.value
        )

        response = frame.send(DEFAULT_DISCOVERY_ADDRESS, verbose=verbose)

        return response
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
