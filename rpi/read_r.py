from statistics import mean
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

a_pin = 16
b_pin = 18


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
    for i in range(10):
        x.append(analog_read())
        time.sleep(0.05)
    x = sum(x) / len(x)

    # x = sorted(x)[3:6]
    x = (x - 100) / 300
    if x < 0:
        x = 0
    if x > 2:
        x = 2
    print(x)

    # print(analog_read())
    # time.sleep(0.1)
