#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from precise_runner import PreciseEngine, PreciseRunner
import threading

class ControllerFunction:
    def __init__(self, pb_file, gpio_pin=None, on_activation=None):
        self.pb_file = pb_file
        self.gpio_pin = gpio_pin
        self.on_activation = on_activation
        self.GPIO = GPIO
        if self.gpio_pin is not None:
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setup(self.gpio_pin, self.GPIO.OUT)
        self.is_running = False

    def start_runner(self):
        def activation_callback():
            if self.on_activation is not None:
                self.on_activation(self.gpio_pin)

        engine = PreciseEngine('precise-engine/precise-engine', self.pb_file)
        runner = PreciseRunner(engine, on_activation=activation_callback)

        self.is_running = True
        while self.is_running:
            runner.start()

    def stop_runner(self):
        self.is_running = False


def stop(objects):
    for obj in objects:
        obj.stop()
        sleep(1.2)
        obj.start()

def start(objects):
    for obj in objects:
        obj.start()


def external_on_activation(gpio_pin):
    def on_activation(pin):
        print(f'Detected on GPIO pin {pin}')
        # Additional logic for controlling the LED using the GPIO pin

    return lambda pin: on_activation(gpio_pin)


if __name__ == '__main__':
    Up = ControllerFunction('Up.pb', 17, external_on_activation(17))
    Down = ControllerFunction('Down.pb', 27, external_on_activation(27))
    Stop = ControllerFunction('Stop.pb', on_activation=external_on_activation(None))
    objects = [Up, Down, Stop]


    # Start each runner in a separate thread
    threads = []
    for obj in objects:
        thread = threading.Thread(target=obj.start_runner)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Stop all runners
    stop(objects)

    # Sleep forever
    from time import sleep
    while True:
        sleep(10)
