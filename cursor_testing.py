
from psychopy import visual, core, event
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import numpy as np
import pandas as pd
from funcs import *


# ------------------------ Function and constant var set up ---------------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
timeLimit = 3
max_volt = 5


# ---------- Main Experiment Run -------------------------------------------------
# Create your Phidget channels
ch0 = config_channel(2, 100)
ch1 = config_channel(1, 100)

# Do stuff with your Phidgets here or in your event handlers.
mywin = visual.Window(fullscr=True, monitor='testMonitor',
                      units='pix', color='black')


# Makes cursors and targets
int_cursor = visual.Circle(
    mywin, radius=cm_to_pixel(cursor_size), fillColor='green')  # integrated pos
target = visual.Circle(
    mywin, radius=cm_to_pixel(target_size), fillColor='blue')  # initial target
home = visual.Circle(
    mywin, radius=cm_to_pixel(home_size), lineColor='red')


while True:
    update_pos(get_pos(ch0, ch1), int_cursor)
    mywin.flip()
    home.draw()

    # stop if button press
    if len(event.getKeys()) > 0:
        break
    event.clearEvents()


# Close the channels once the program is done.
ch0.close()
ch1.close()
