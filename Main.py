#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin python

#For local directory
from os.path import dirname, abspath
dir = dirname(dirname(abspath(__file__))) + "/Voice-Activated-Remote"
import RPi.GPIO as GPIO
import time
import threading
from precise_runner import PreciseEngine, PreciseRunner

# Relay Control Pins
CHAIR_UP = 17 #M1 + 
CHAIR_DOWN = 27 #M1 - 
HEAD_UP = 10 #M2 + 
HEAD_DOWN = 22 #M3 -

OPERATING_TIME = 3 # Seconds for each operation

STACK_LEN = 5 # Number of commands that can be stacked

# Set GPIO Numbering Mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins as outputs
GPIO.setup(CHAIR_UP, GPIO.OUT)
GPIO.setup(CHAIR_DOWN, GPIO.OUT)
GPIO.setup(HEAD_UP, GPIO.OUT)
GPIO.setup(HEAD_DOWN, GPIO.OUT)

# Stack to hold incoming commands
command_stack = []




# Function to activate Motors

# Supported Operations C-UP, Chair Up
#                      C-DW, Chair Down
#                      H-UP, Headrest Up
#                      H-DW, Headrest Down

def operation(operation, OPERATING_TIME):
    pin = 00
    thread = threading.current_thread()  # Get the current thread
    thread.stop_flag = False  # Initialize the stop flag
    if operation == "C-UP":
        pin = CHAIR_UP
        start_time = time.time()
        while not thread.stop_flag:  # Check the stop flag to stop the loop
            print("C-UP")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(OPERATING_TIME)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(OPERATING_TIME)

    elif operation == "C-DW":
        pin = CHAIR_DOWN
        start_time = time.time()
        while not thread.stop_flag:
            print("C-DW")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(OPERATING_TIME)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(OPERATING_TIME)

    elif operation == "H-UP":
        pin = HEAD_UP

    elif operation == "H-DW":
        pin = HEAD_DOWN   

    while True:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(OPERATING_TIME)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(OPERATING_TIME)

def kill_all_pins():
    GPIO.output(CHAIR_UP, GPIO.LOW)
    GPIO.output(CHAIR_DOWN, GPIO.LOW)
    GPIO.output(HEAD_UP, GPIO.LOW)
    GPIO.output(HEAD_DOWN, GPIO.LOW)


# Function to add commands to stack 
def add_to_stack(operation, OPERATING_TIME):
    # Only allows 5 commands to be stacked
    if len(command_stack) >= STACK_LEN:
        return
    thread = threading.Thread(target=operation, args=(operation, OPERATING_TIME))
    command_stack.append(thread)


# Function to remove completed threads from stack
def remove_completed_threads():
    while True:
        for thread in command_stack:
            if not thread.is_alive():
                command_stack.remove(thread)
        time.sleep(1)  # Adjust the sleep duration as needed


# Function to stop operation 
def stop():
    kill_all_pins()
    for thread in command_stack:
        thread.stop_flag = True  # Set the stop flag in the thread
    command_stack.clear()



# Function to track chair position
def track_position():
    global chair_position
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if command_stack:  # Check if command_stack is not empty
            if command_stack[-1].is_alive():  # Check if the last command thread is still running
                if command_stack[-1].operation == "C-UP":
                    chair_position = int(elapsed_time)  # Track chair position in seconds
                elif command_stack[-1].operation == "C-DW":
                    chair_position = max(0, chair_position - int(elapsed_time))  # Subtract elapsed_time from position, but ensure it doesn't go below 0
        time.sleep(1)  # Update position every second




# Engines and Runners for Recognition

engine1 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Up/Up.pb')
runner1 = PreciseRunner(engine1, on_activation=add_to_stack("C-UP", OPERATING_TIME))
runner1.start()

engine2 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Down/Down.pb')
runner2 = PreciseRunner(engine2, on_activation=add_to_stack("C-DW", OPERATING_TIME))
runner2.start()


engine4 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Up/Headrest-Up.pb')
runner4 = PreciseRunner(engine4, on_activation=add_to_stack("H-UP", OPERATING_TIME))
runner4.start()


engine5 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Down/Headrest-Down.pb')
runner5 = PreciseRunner(engine5, on_activation=add_to_stack("H-DW", OPERATING_TIME))
runner5.start()

engine3 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stop/Stop.pb')
runner3 = PreciseRunner(engine3, on_activation=stop())
runner3.start()


# Start Thread to clear completed threads
remove_threads_thread = threading.Thread(target=remove_completed_threads)
remove_threads_thread.start()

# Start Thread to track chair position
position_thread = threading.Thread(target=track_position)
position_thread.start()


# Sleep forever
from time import sleep
while True:
    sleep(10)
