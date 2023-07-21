#!/home/z25/Desktop/Voice-Activated-Remote/.venv/bin python

# For local directory
from os.path import dirname, abspath
dir = dirname(dirname(abspath(__file__))) + "/Voice-Activated-Remote"
import RPi.GPIO as GPIO
import time
import threading
from precise_runner import PreciseEngine, PreciseRunner

# Button Pin Assignment
BT_CHAIR_UP = 17
BT_CHAIR_DOWN = 27
BT_HEADREST_UP = 22
BT_HEADREST_DOWN = 10

# Relay Pin Assignment
RE_M1_PLUS = 14
RE_M1_MINUS = 15
RE_M2_PLUS = 18
RE_M2_MINUS = 23

# Variables to keep track of positions
POS_CHAIR_CUR = 0  # Current Position of Chair
POS_CHAIR_TAR = 0  # Target Position of Chair

POS_HEAD_CUR = 0  # Current Position of Headrest
POS_HEAD_TAR = 0  # Target Position of Headrest

OPERATING_TIME = 5  # Num Seconds for each voice-activated movement
STACK_LEN = 5  # Amount of Stackable Commands

# Global variables
current_operation = None
ignore_button_events = False  # Flag to ignore button events while executing voice commands

GPIO.setmode(GPIO.BCM)

# GPIO Setup for Buttons
GPIO.setup(BT_CHAIR_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BT_CHAIR_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BT_HEADREST_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BT_HEADREST_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO Setup for Relays
GPIO.setup(RE_M1_PLUS, GPIO.OUT)
GPIO.setup(RE_M1_MINUS, GPIO.OUT)
GPIO.setup(RE_M2_PLUS, GPIO.OUT)
GPIO.setup(RE_M2_MINUS, GPIO.OUT)

# Stack to hold incoming commands
command_stack = []

def execute(operation):
    global ignore_button_events 
    ignore_button_events = True
    pin = 0
    if operation == "STOP":  # Check for "stop" operation
        stopAll()
    
    elif operation == "C-UP":
        pin = RE_M1_MINUS
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(OPERATING_TIME)
        GPIO.output(pin, GPIO.LOW)

    elif operation == "C-DW":
        pin = RE_M1_PLUS
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(OPERATING_TIME)
        GPIO.output(pin, GPIO.LOW)

    elif operation == "H-UP":
        pin = RE_M2_MINUS
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(OPERATING_TIME)
        GPIO.output(pin, GPIO.LOW)

    elif operation == "H-DW":
        pin = RE_M2_PLUS
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(OPERATING_TIME)
        GPIO.output(pin, GPIO.LOW)
    
    elif operation == "STAND":
        pin = RE_M1_MINUS
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(25)
        GPIO.output(pin, GPIO.LOW)
    
    elif operation == "SLEEP":
        pin = RE_M1_PLUS
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(RE_M2_PLUS, GPIO.HIGH)
        time.sleep(25)
        GPIO.output(RE_M2_PLUS, GPIO.LOW)
        GPIO.output(pin, GPIO.LOW)
    
    ignore_button_events = False
    # Remove the current thread from the command_stack
    command_stack.remove(threading.current_thread())

# Function to add commands to stack 
def add_to_stack(operation):
    thread = threading.Thread(target=execute, args=(operation,))
    command_stack.append(thread)
    
    # Set the current operation
    global current_operation
    current_operation = operation
    
    thread.start()

# Function to remove completed threads from stack
def remove_completed_threads():
    while True:
        for thread in command_stack.copy():
            if not thread.is_alive() and thread not in threading.enumerate():
                if thread in command_stack:
                    command_stack.remove(thread)
        time.sleep(1)

def kill_all_pins():
    GPIO.output(RE_M2_MINUS, GPIO.LOW)
    GPIO.output(RE_M2_PLUS, GPIO.LOW)
    GPIO.output(RE_M1_MINUS, GPIO.LOW)
    GPIO.output(RE_M1_PLUS, GPIO.LOW)

def chairUp():
    add_to_stack("C-UP")
    print("CHAIR UP")

def chairDown():
    add_to_stack("C-DW")
    print("CHAIR DOWN")

def headrestDown():
    add_to_stack("H-DW")
    print("HEADREST DOWN")

def headrestUp():
    add_to_stack("H-UP")
    print("HEADREST UP")

def stand():
    add_to_stack("STAND")
    print("STAND")

def sleep():
    add_to_stack("SLEEP")
    print("SLEEP")

def stopAll():
    global ignore_button_events
    ignore_button_events = False
    kill_all_pins()
    print("STOP")

def chairUPButtonChanged(channel):
    global ignore_button_events
    if not ignore_button_events:
        if GPIO.input(channel) == GPIO.LOW:
            print('Chair Up Button Pressed')
            GPIO.output(RE_M1_MINUS, GPIO.HIGH)
        else:
            print('Chair Up Button Released')
            GPIO.output(RE_M1_MINUS, GPIO.LOW)

def chairDOWNButtonChanged(channel):
    global ignore_button_events
    if not ignore_button_events:
        if GPIO.input(channel) == GPIO.LOW:
            print('Chair Down Button Pressed')
            GPIO.output(RE_M1_PLUS, GPIO.HIGH)
        else:
            print('Chair Down Button Released')
            GPIO.output(RE_M1_PLUS, GPIO.LOW)

def headrestUPButtonChanged(channel):
    global ignore_button_events
    if not ignore_button_events:
        if GPIO.input(channel) == GPIO.LOW:
            print('Headrest Up Button Pressed')
            GPIO.output(RE_M2_MINUS, GPIO.HIGH)
        else:
            print('Headrest Up Button Released')
            GPIO.output(RE_M2_MINUS, GPIO.LOW)

def headrestDOWNButtonChanged(channel):
    global ignore_button_events
    if not ignore_button_events:
        if GPIO.input(channel) == GPIO.LOW:
            print('Headrest Down Button Pressed')
            GPIO.output(RE_M2_PLUS, GPIO.HIGH)
        else:
            print('Headrest Down Button Released')
            GPIO.output(RE_M2_PLUS, GPIO.LOW)

DEBOUNCE_TIME = 200

# Add event detection for chair up button
GPIO.add_event_detect(BT_CHAIR_UP, GPIO.BOTH, callback=chairUPButtonChanged, bouncetime=DEBOUNCE_TIME)

# Add event detection for chair down button
GPIO.add_event_detect(BT_CHAIR_DOWN, GPIO.BOTH, callback=chairDOWNButtonChanged, bouncetime=DEBOUNCE_TIME)

# Add event detection for headrest up button
GPIO.add_event_detect(BT_HEADREST_UP, GPIO.BOTH, callback=headrestUPButtonChanged, bouncetime=DEBOUNCE_TIME)

# Add event detection for headrest down button
GPIO.add_event_detect(BT_HEADREST_DOWN, GPIO.BOTH, callback=headrestDOWNButtonChanged,  bouncetime=DEBOUNCE_TIME)

engine1 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Chair Up/ChairUp.pb')
runner1 = PreciseRunner(engine1, on_activation=chairUp)
runner1.start()

engine2 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Chair Down/ChairDown.pb')
runner2 = PreciseRunner(engine2, on_activation=chairDown)
runner2.start()

engine3 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Up/HeadrestUp.pb')
runner3 = PreciseRunner(engine3, on_activation=headrestUp)
runner3.start()

engine4 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Headrest Down/HeadrestDown.pb')
runner4 = PreciseRunner(engine4, on_activation=headrestDown)
runner4.start()

engine5 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stop/Stop.pb')
runner5 = PreciseRunner(engine5, on_activation=stopAll)  # Use stopAll function
runner5.start()

engine6 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Khursee Ninche/KN.pb')
runner6 = PreciseRunner(engine6, on_activation=chairDown)
runner6.start()


engine7 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Sleep/Sleep.pb')
runner7 = PreciseRunner(engine7, on_activation=sleep)
runner7.start()

engine8 = PreciseEngine(dir + '/precise-engine/precise-engine', dir + '/Models/Stand/Stand.pb')
runner8 = PreciseRunner(engine8, on_activation=stand)
runner8.start()

# Start Thread to clear completed threads
remove_threads_thread = threading.Thread(target=remove_completed_threads)
remove_threads_thread.start()

# Sleep forever
while True:
    time.sleep(10)
