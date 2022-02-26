import asyncio
import sys
import json
sys.path.append("../hardware_output")
from serial_comms import SerialCommunicator

ser_comms = SerialCommunicator()

async def handle_echo(reader, writer):
    data = await reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    # variables
    target = "person"
    signal = 0

    print(message)
    detections = json.loads(message)
    print(signal)
    # signal = (dist/diagonal) * 255

    # if "person" in detections['labels']:
    #     ser_comms.write_signal(0)
    # else:
    #     ser_comms.write_signal(255)
    # print(detections)

    print(f"Send: thumbs up")
    writer.write("thumbs up".encode())
    await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())