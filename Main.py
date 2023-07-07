#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin python

# For local directory
from os.path import dirname, abspath
import RPi.GPIO as GPIO
import time
import threading
from precise_runner import PreciseEngine, PreciseRunner

# Relay Control Pins
CHAIR_UP = 17  # M1 +
CHAIR_DOWN = 27  # M1 -
HEAD_UP = 10  # M2 +
HEAD_DOWN = 22  # M3 -

OPERATING_TIME = 3  # Seconds for each operation

STACK_LEN = 5  # Number of commands that can be stacked

# Set GPIO Numbering Mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins as outputs
GPIO.setup(CHAIR_UP, GPIO.OUT)
GPIO.setup(CHAIR_DOWN, GPIO.OUT)
GPIO.setup(HEAD_UP, GPIO.OUT)
GPIO.setup(HEAD_DOWN, GPIO.OUT)

# Stack to hold incoming commands
command_stack = []
chair_position = 0  # Track chair position


# Function to activate Motors

# Supported Operations C-UP, Chair Up
#                      C-DW, Chair Down
#                      H-UP, Headrest Up
#                      H-DW, Headrest Down

def perform_operation(operation, operating_time):
    global chair_position
    pin = None
    if operation == "C-UP":
        pin = CHAIR_UP
        chair_position += operating_time
    elif operation == "C-DW":
        pin = CHAIR_DOWN
        chair_position = max(0, chair_position - operating_time)
    elif operation == "H-UP":
        pin = HEAD_UP
    elif operation == "H-DW":
        pin = HEAD_DOWN

    if pin is not None:
        start_time = time.time()
        while time.time() - start_time < operating_time:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)


def kill_all_pins():
    GPIO.output(CHAIR_UP, GPIO.LOW)
    GPIO.output(CHAIR_DOWN, GPIO.LOW)
    GPIO.output(HEAD_UP, GPIO.LOW)
    GPIO.output(HEAD_DOWN, GPIO.LOW)


# Function to add commands to stack
def add_to_stack(operation, operating_time):
    # Only allows 5 commands to be stacked
    if len(command_stack) >= STACK_LEN:
        return
    command_stack.append((operation, operating_time))


# Function to process commands from the stack
def process_commands():
    while True:
        if command_stack:
            operation, operating_time = command_stack.pop(0)
            perform_operation(operation, operating_time)
        time.sleep(0.1)  # Adjust the sleep duration as needed


# Function to stop operation
def stop():
    kill_all_pins()
    command_stack.clear()
    chair_position = 0


# Wrapper function for add_to_stack with arguments
def add_to_stack_wrapper(operation, operating_time):
    print("Hello")
    add_to_stack(operation, operating_time)


# Engines and Runners for Recognition
dir = dirname(dirname(abspath(__file__))) + "/Voice-Activated-Remote"

engine1 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Up/Up.pb')
runner1 = PreciseRunner(engine1, on_activation=lambda: add_to_stack_wrapper("C-UP", OPERATING_TIME))
runner1.start()

engine2 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Down/Down.pb')
runner2 = PreciseRunner(engine2, on_activation=lambda: add_to_stack_wrapper("C-DW", OPERATING_TIME))
runner2.start()

engine3 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stop/Stop.pb')
runner3 = PreciseRunner(engine3, on_activation=stop)
runner3.start()


# Start Thread to process commands
process_commands_thread = threading.Thread(target=process_commands)
process_commands_thread.start()

# Start Thread to track chair position
def track_position():
    global chair_position
    while True:
        if command_stack and command_stack[-1][0] == "C-UP":
            elapsed_time = time.time() - command_stack[-1][1]
            chair_position = int(elapsed_time)
        elif command_stack and command_stack[-1][0] == "C-DW":
            elapsed_time = time.time() - command_stack[-1][1]
            chair_position = max(0, chair_position - int(elapsed_time))
        time.sleep(1)

position_thread = threading.Thread(target=track_position)
position_thread.start()

# Sleep forever
while True:
    time.sleep(10)
