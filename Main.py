#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin python

#For local directory
from os.path import dirname, abspath
dir = dirname(dirname(abspath(__file__))) + "/Voice-Activated-Remote"
import RPi.GPIO as GPIO
import time
from precise_runner import PreciseEngine, PreciseRunner

LED_UP = 17
LED_DOWN = 27
LED_STOP = 10
LED_PRESET = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_UP, GPIO.OUT)
GPIO.setup(LED_DOWN, GPIO.OUT)
GPIO.setup(LED_STOP, GPIO.OUT)
GPIO.setup(LED_PRESET, GPIO.OUT)

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

def on_activation3():
    print('Stop Detected')
    GPIO.output(LED_STOP, GPIO.HIGH)
    time.sleep(1);
    GPIO.output(LED_STOP, GPIO.LOW)

def on_activation4():
    print('Preset Detected')
    GPIO.output(LED_PRESET, GPIO.HIGH)
    time.sleep(1);
    GPIO.output(LED_PRESET, GPIO.LOW)




engine1 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Up/Up.pb')
runner1 = PreciseRunner(engine1, on_activation=on_activation1)
runner1.start()

engine2 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Down/Down.pb')
runner2 = PreciseRunner(engine2, on_activation=on_activation2)
runner2.start()


engine3 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stop/Stop.pb')
runner3 = PreciseRunner(engine3, on_activation=on_activation3)
runner3.start()


engine4 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Up/Headrest-Up.pb')
runner4 = PreciseRunner(engine4, on_activation=on_activation4)
runner4.start()


engine5 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Down/Headrest-Down.pb')
runner5 = PreciseRunner(engine5, on_activation=on_activation4)
runner5.start()

engine6 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Sit/Sit.pb')
runner6 = PreciseRunner(engine6, on_activation=on_activation4)
runner6.start()

engine7 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/TV/TV.pb')
runner7 = PreciseRunner(engine7, on_activation=on_activation4)
runner7.start()

engine8 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Sleep/Sleep.pb')
runner8 = PreciseRunner(engine8, on_activation=on_activation4)
runner8.start()

engine9 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stand/Stand.pb')
runner9 = PreciseRunner(engine9, on_activation=on_activation4)
runner9.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)
