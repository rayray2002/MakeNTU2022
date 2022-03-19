import RPi.GPIO as GPIO
import threading
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


MOTOR_PIN = 32
R_PIN_A = 16
R_PIN_B = 18


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

    x = (x - 100) / 300
    if x < 0:
        x = 0
    if x > 2:
        x = 2
    return x


if __name__ == "__main__":
    motor = setup()
    SM = pd.read_csv("../data/F.csv", header=0)
    usage = [0]
    electricityRecord = []
    fig, ax = plt.subplots(2, 1)
    usagePlot = ax[0]
    electricityPlot = ax[1]

    # print(SM.head())

    for index, row in SM.iterrows():
        if index % 6 != 0:
            continue

        ratio = measure()
        # print(row)
        instanceElectricity = row["instanceElectricity"]
        dt = datetime.fromtimestamp(row["time"] + 1643587200)

        electricity = instanceElectricity * ratio
        electricityRecord.append(electricity)
        usage.append((usage[-1] + electricity / 2000))
        power = max(min(electricity / 50, 100), 0)
        print(f"{ratio:.2f}, {power:.2f}, {dt}, {electricity:.2f}")

        motor.ChangeDutyCycle(power)

        if index % 288 == 0:
            usagePlot.plot(usage, color="b")
            usagePlot.axvline(x=len(usage), color="k", linestyle="--")

            electricityPlot.plot(electricityRecord, color="r")
            electricityPlot.axvline(x=len(electricityRecord), color="k", linestyle="--")
            plt.savefig("plot.png")
            # plt.clf()

        # time.sleep(0.5)
