#!/usr/bin/env python3
from precise_runner import PreciseEngine, PreciseRunner

def on_activation1():
    print('Up Detected')

def on_activation2():
    print('Down Detected')

def on_activation3():
    print('Close Detected')

def on_activation4():
    print('Down Detected')



engine1 = PreciseEngine('precise-engine/precise-engine', 'Up.pb')
runner1 = PreciseRunner(engine1, on_activation=on_activation1)
runner1.start()

engine2 = PreciseEngine('precise-engine/precise-engine', 'Down.pb')
runner2 = PreciseRunner(engine2, on_activation=on_activation2)
runner2.start()


# Sleep forever
from time import sleep
while True:
    sleep(10)