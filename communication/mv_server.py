import asyncio
from os import device_encoding
import sys
import json
from threading import Thread

sys.path.append("../hardware_output")
from serial_comms import SerialCommunicator

sys.path.append("../")
from voicedetection import Recogniser, recognize_speech_from_mic

ser_comms = SerialCommunicator()
recogniser = Recogniser(device_index=19)
target = None
recognised_label = None

def set_target():
    global target
    global recognised_label
    while 1:
        ser_comms.read_signal()
        # insert change of target here!
        print("RECOGNISING")
        known, recognised_label = recogniser.get_voice_input()
        if known:
            target = label
        else:
            target = None

thread = Thread(target = set_target)
thread.start()


async def handle_echo(reader, writer):
    data = await reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    # variables
    signal = 255

    detections = json.loads(message)
    for i, label in enumerate(detections["labels"]):
        if label == target:
            curr_signal = (1 - detections["distance_ratio"][i]) * 255
            signal = min(signal, int(curr_signal))


    print(signal, target, recognised_label)
    ser_comms.put(signal)

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