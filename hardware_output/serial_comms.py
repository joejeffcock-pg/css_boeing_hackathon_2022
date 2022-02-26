import serial
import sys
from threading import Thread
from queue import Queue
import time

class SerialCommunicator:
    def __init__(self, name="/dev/ttyACM0", baud=9600):
        self.ser = serial.Serial(name, baud)
        self.queue = Queue()
        self.thread = Thread(target=self.mainloop)
        self.thread.start()

    def mainloop(self):
        while 1:
            signal = None
            while not self.queue.empty():
                signal = self.queue.get()

            if signal is not None:
                self.write_signal(self.queue.get())

            time.sleep(0.05) # 20hz

    def write_signal(self, signal):
        payload = (signal).to_bytes(1, "big")
        self.ser.write(payload)

    def read_signal(self):
        signal = self.ser.read()
        return int.from_bytes(signal, "big")

    def put(self, data):
        self.queue.put(data)
