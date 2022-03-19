#!/usr/bin/env python3
import serial
import threading


class arduinoReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()

    def run(self):
        out = [0, 0, 0, 0, 0, 0]
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip("\r")

                try:
                    line = line.split(",")
                    id = int(line[0])
                    value = int(line[1])
                    out[id] = value
                    print(id, value)
                except:
                    pass

if __name__ == "__main__":
    reader = arduinoReader()
    while True:
        input()
        reader.readArduino()
