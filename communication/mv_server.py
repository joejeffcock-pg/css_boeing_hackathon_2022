import asyncio
import sys
import json
sys.path.append("../hardware_output")
from serial_comms import SerialCommunicator
from threading import Thread

ser_comms = SerialCommunicator()

def set_target():
    while 1:
        ser_comms.read_signal()
        # insert change of target here!
        print("button pressed")

thread = Thread(target = set_target)
thread.start()


async def handle_echo(reader, writer):
    data = await reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    # variables
    target = "person"
    signal = 255

    detections = json.loads(message)
    for i, label in enumerate(detections["labels"]):
        if label == target:
            curr_signal = (1 - detections["distance_ratio"][i]) * 255
            signal = min(signal, int(curr_signal))


    print(signal)
    ser_comms.put(signal)

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