"""
Networking interface
Interfaces with the server that the satalite will connect to.
"""

import asyncio
import json

class Client():
    """ Client

    This class holds the functions to interact with the server side.
    """
    def __init__(self, ip_address = "localhost", port = 50007):
        self.ip_address = ip_address
        self.port = port
        return

    async def send_data(self, data: dict):
        """Sends data to the server to be sent to the satallite"""
        packet = "~GUI~"
        packet += json.dumps(data)

        reader, writer = await asyncio.open_connection(self.ip_address, self.port)

        print(f"sending message: {packet}")
        writer.write(packet.encode("utf8"))
        await writer.drain()

        writer.close()
        await writer.wait_closed()
