"""
Sets up the IR remote control and allows signals sent by it to be read
for a Raspberry Pi 4 Model B.

NOTE: This requires lirc to be set up before use.
"""

# Import the LIRC library
import lirc

def initialize_ir(to=None):
    """
    Initializes the IR remote control.

    Inputs:
        to: An integer representing the timeout length. This means that
        if the IR control does not receive a signal after `to` seconds,
        then it will close the connection.
    Returns: 
        client: An LIRC connection class from the LIRC library.
        This refers to the IR remote being used.
    """
    client = lirc.LircdConnection(timeout=to)
    client.connect()

    return client

def read_ir(client):
    """
    Reads signals from the IR client. Note that this will stop the
    program until a signal is received.

    Inputs:
        client: An LIRC connection class from the LIRC library.
        This refers to the IR remote being used.
    
    Returns:
        command: A string representing the signal sent by the IR 
        remote.
    """
    line = client.readline()
    if line:
        command = line.split()[2]
        return command
    else: 
        return None