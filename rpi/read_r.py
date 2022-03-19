from statistics import mean
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

a_pin = 18
b_pin = 23


def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)


def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count + 1
    return count


def analog_read():
    discharge()
    return charge_time()


while True:
    x = []
    for i in range(20):
        x.append(analog_read())
    y = sorted(x)
    sum = 0
    for j in range(7):
        sum += y[j + 7]
    mean = sum / 7
    print(mean)
    time.sleep(1)
