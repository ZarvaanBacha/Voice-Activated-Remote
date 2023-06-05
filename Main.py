#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin pytho

#For local directory
from os.path import dirname, abspath
dir = dirname(dirname(abspath(__file__)))
import RPi.GPIO as GPIO
import time
from precise_runner import PreciseEngine, PreciseRunner

LED_UP = 17
LED_DOWN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_UP, GPIO.OUT)
GPIO.setup(LED_DOWN, GPIO.OUT)

def on_activation1():
    print('Up Detected')
    GPIO.output(LED_UP, GPIO.HIGH)
    time.sleep(1);
    GPIO.output(LED_UP, GPIO.LOW)

def on_activation2():
    print('Down Detected')
    GPIO.output(LED_DOWN, GPIO.HIGH)
    time.sleep(1);
    GPIO.output(LED_DOWN, GPIO.LOW)





engine1 = PreciseEngine(dir + '/Voice-Activated-Remote/precise-engine/precise-engine', 'Up.pb')
runner1 = PreciseRunner(engine1, on_activation=on_activation1)
runner1.start()

engine2 = PreciseEngine(dir + '/Voice-Activated-Remote/precise-engine/precise-engine', 'Down.pb')
runner2 = PreciseRunner(engine2, on_activation=on_activation2)
runner2.start()


# Sleep forever
from time import sleep
while True:
    sleep(10)
