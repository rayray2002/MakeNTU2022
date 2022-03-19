import RPi.GPIO as GPIO
import threading
import time
import pandas as pd
import numpy as np
import serial
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
# from arduino import *
pd.options.mode.chained_assignment = None


MOTOR_PIN = 32
R_PIN_A = 16
R_PIN_B = 18

ratio = 0
ratios = [0, 0, 0, 0, 0, 0]



def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_PIN, GPIO.OUT, initial=GPIO.LOW)
    motor = GPIO.PWM(MOTOR_PIN, 1000)
    motor.start(0)
    return motor


def discharge():
    GPIO.setup(R_PIN_A, GPIO.IN)
    GPIO.setup(R_PIN_B, GPIO.OUT)
    GPIO.output(R_PIN_B, False)
    time.sleep(0.005)


def charge_time():
    GPIO.setup(R_PIN_B, GPIO.IN)
    GPIO.setup(R_PIN_A, GPIO.OUT)
    count = 0
    GPIO.output(R_PIN_A, True)
    while not GPIO.input(R_PIN_B):
        count = count + 1
    return count


def analog_read():
    discharge()
    return charge_time()


def measure():
    x = []
    for i in range(10):
        x.append(analog_read())
        time.sleep(0.05)
    x = sum(x) / len(x)

    x = min(max((x - 100) / 300, 0), 2)
    return x


class arduinoReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()

    def run(self):
        global ratios
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip("\r")

                try:
                    line = line.split(",")
                    id = int(line[0])
                    value = float(line[1])/512
                    ratios[id] = value
                    # print(id, value)
                except:
                    pass



if __name__ == "__main__":
    motor = setup()
    reader = arduinoReader()
    reader.start()
    SM = pd.read_csv("SM.csv", header=0)

    # print(SM.head())

    usage = []
    electricityRecord = []
    date = []

    fig, ax = plt.subplots(2, 1, figsize=(8, 6))
    usagePlot = ax[0]
    electricityPlot = ax[1]
    daySep = []

    noise = np.random.normal(1, scale=0.1, size=48)
    # print(noise)

    # measure.start()

    # print(SM.head())

    for index, row in SM.iterrows():
        # if index % 12 != 0:
        #     continue

        if len(usage) % 24 == 0:
            daySep.append(len(usage))

        ratio = ratios[0]
        print(ratios)

        instanceElectricity = row["instanceElectricity"]
        # dt = datetime.fromtimestamp(row["time"] + 1643587200).strftime("%m/%d %H:%M")
        date.append(row["time"])

        pred = SM.iloc[len(usage) : len(usage) + 48, :]
        pred.iloc[0, 1] = instanceElectricity
        pred["instanceElectricity"] = pred["instanceElectricity"] * ratio
        pred["instanceElectricity"] = pred["instanceElectricity"].multiply(
            noise, axis=0
        )

        print(pred["instanceElectricity"].sum()/1000*15)

        electricity = instanceElectricity * ratio
        electricityRecord.append(electricity)
        if len(usage):
            usage.append((usage[-1] + electricity / 2000))
        else:
            usage.append(electricity / 2000)
        power = max(min(electricity / 50, 100), 0)
        print(f"{ratio:.2f}, {power:.2f}, {row['time']}, {electricity:.2f}")


        motor.ChangeDutyCycle(power)

        usagePlot.plot(date, usage, color="b")
        electricityPlot.plot(date, electricityRecord, color="r")
        electricityPlot.plot(
            pred["time"],
            pred["instanceElectricity"],
            color="tab:orange",
            linestyle="--",
        )

        for sep in daySep:
            usagePlot.axvline(x=sep, color="k", linestyle="--")
            electricityPlot.axvline(x=sep, color="k", linestyle="--")

        tmp = len(usage) // 10 + 1
        xticks = date[::tmp]

        electricityPlot.set_xticks(xticks)
        usagePlot.set_xticks(xticks)

        fig.autofmt_xdate()
        plt.savefig("plot.png")

        usagePlot.cla()
        electricityPlot.cla()

        # time.sleep(0.1)
