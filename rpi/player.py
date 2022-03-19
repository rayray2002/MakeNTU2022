import RPi.GPIO as GPIO
import threading
import time

MOTOR_PIN = 32

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_PIN, GPIO.OUT, initial=GPIO.LOW)
    motor = GPIO.PWM(MOTOR_PIN, 100)
    motor.start(0)
    return motor


if __name__ == "__main__":
    motor = setup()
    while True:
        for i in range(100):
            motor.ChangeDutyCycle(i)
            time.sleep(0.1)
