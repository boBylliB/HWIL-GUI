"""
Networking Functionality
THIS SHOULD RUN ON ITS OWN, THE GUI WILL INTERACT WITH IT
"""

import asyncio
import csv
import datetime

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
        self.socket = await asyncio.start_server(
            self.handle_conn,
            self.ip_address,
            self.port)

        async with self.socket:
            await self.socket.serve_forever()
        return

    async def handle_conn(self, reader, writer):
        request = None
        request = (await reader.read(1024)).decode('utf8')
        if "~GUI~" in request:
            print("From GUI")
            print(str(request))
        else:
            print("From Satallite")
            print(str(request))
            await self.handle_data(request)
        writer.close()
        return

    async def handle_data(self, request):
        data = request.split(',')
        for point in data:
            num = point.split('=')
            self.write_csv(num[0],num[1])
        return

    def write_csv(self, var_name, data_point):
        var_name+=".csv"
        row = [datetime.datetime.now(), data_point]
        with open(var_name, 'w', encoding = 'utfa') as csvfile:
            csvwriter = csv.writer(csvfile)
            # writing the fields (column)
            csvwriter.writerow(row)

    async def handle_gui(self, request):
        """Handles commands from GUI"""
        command = request[4:request.len() + 1]
        if command.startswith("write"):
            self.client_send = command[5:request.len]
        elif command.startswith("video"):
            print("sending video")
            # TODO: Figure out how video data will be sent and channel it correctly
        return

async def main():
    srv = Server()
    await srv.start_server()


asyncio.run(main())
