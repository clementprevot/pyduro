# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------

from constants import DEFAULT_DISCOVERY_ADDRESS
from protocol import FUNCTIONS, PAYLOADS, FunctionNotFoundException, PayloadToLargeException
from protocol.frame import Frame

#-----------------------------------------------------------------------------------------------------------------------

def run():
    """
    Run the discovery of burner(s) in the local network.
    This trigger a specific "Discovery" frame on an UDP broadcat and wait for any burner(s) to send back a response
    """

    try:
        frame = Frame('<serial>', '<pin>', FUNCTIONS.discover.value, PAYLOADS.discovery.value)

        response = frame.send(DEFAULT_DISCOVERY_ADDRESS)
        if not response:
            print('No burner answered to the discover answer in less than 5 seconds...')
        else:
            print(response.frame)
    except FunctionNotFoundException as e:
        print(e.message)
    except PayloadToLargeException as e:
        print(e.message)
