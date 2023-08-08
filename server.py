"""
Server Code
THIS SHOULD RUN ON ITS OWN, THE GUI WILL INTERACT WITH IT
"""

import asyncio
import csv
import datetime
import json

class Server():
    """ Networking Interface

    This class holds all things related to networking

    Attributes
    ----------
    IP: str
        Holds the IP the program binds to\n
    PORT: int
        Holds the port to bind to
    """
    def __init__(self, ip_address = "0.0.0.0", port = 50007):
        self.ip_address = ip_address
        self.port = port
        self.socket = None
        self.client_send = None


    async def start_server(self):
        """ Start Server

        Starts the server up for connections
        """
        self.socket = await asyncio.start_server(
            self.handle_conn,
            self.ip_address,
            self.port)

        async with self.socket:
            await self.socket.serve_forever()
        return

    async def handle_conn(self, reader, writer):
        """ Handle Connection

        Handles the connections to the server:
        If from GUI, handle the data that needs to be sent to the satallite
        If from Satallite, handle data by saving it to csv file.
        """
        request = None
        request = (await reader.read(1024)).decode('utf8')
        if "~GUI~" in request:
            print("From GUI:")
            print(str(request))
            await self.handle_gui(request)
        else:
            print("From Satallite:")
            print(str(request))
            await self.handle_data(request)
            if self.client_send is not None:
                writer.write(self.client_send.encode('utf8'))
                await writer.drain()
                self.client_send = None
        writer.close()
        await writer.wait_closed()


    async def handle_gui(self, request):
        """Handles commands from GUI sent via JSON\n
        Sets the data to be sent to the satallite on next connection\n"""
        strdata = request.replace("~GUI~", "")
        data = json.loads(strdata)
        packet = ""
        for key in data:
            packet += f"{key}:{data[key]},"
        self.client_send = packet

    async def handle_data(self, request):
        """Handles data from satallite\n
        Saves data to csv files"""
        data = request.split(',')
        for point in data:
            num = point.split('=')
            self.write_csv(num[0],num[1])
        return

    async def write_csv(self, var_name, data_point):
        """Writes given data to a csv file of the same name with timestamp"""
        var_name+=".csv"
        row = [datetime.datetime.now(), data_point]
        with open(var_name, 'w', encoding = 'utfa') as csvfile:
            csvwriter = csv.writer(csvfile)
            # writing the fields (column)
            csvwriter.writerow(row)


async def main():
    """Starts up the server program"""
    srv = Server()
    await srv.start_server()


asyncio.run(main())
