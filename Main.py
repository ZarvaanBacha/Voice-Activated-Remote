#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin python

#For local directory
from os.path import dirname, abspath
dir = dirname(dirname(abspath(__file__))) + "/Voice-Activated-Remote"
import RPi.GPIO as GPIO
import time
from precise_runner import PreciseEngine, PreciseRunner

M1_P = 17
M1_N = 27
M2_P = 10
M2_N = 22

DURATION = 3 # Duration for Operations

GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_P, GPIO.OUT)
GPIO.setup(M1_N, GPIO.OUT)
GPIO.setup(M2_P, GPIO.OUT)
GPIO.setup(M2_N, GPIO.OUT)

def Up():
    print("Up Detected")
    GPIO.output(M1_P, GPIO.HIGH)
    time.sleep(DURATION)
    GPIO.output(M1_P, GPIO.LOW)

def Down():
    print("Down Detected")
    GPIO.output(M1_N, GPIO.HIGH)
    time.sleep(DURATION)
    GPIO.output(M1_N, GPIO.LOW)


engine1 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Up/Up.pb')
runner1 = PreciseRunner(engine1, on_activation=Up)
runner1.start()

engine2 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Down/Down.pb')
runner2 = PreciseRunner(engine2, on_activation=Down)
runner2.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)
