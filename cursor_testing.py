
from psychopy import visual, core, event
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import numpy as np
import pandas as pd


# ------------------------ Function and constant var set up ---------------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
timeLimit = 3
max_volt = 4.5


def cm_to_pixel(cm):
    return cm * 37.795275591


def pixel_to_cm(pix):
    return pix/37.795275591


def read_trial_data(file_name, sheet=0):
    return pd.read_excel(file_name, sheet_name=sheet)


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setDeviceSerialNumber(678135)
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


def get_pos(ch0, ch1, rot_mat):
    button1 = ch0.getVoltage()/max_volt
    button2 = ch1.getVoltage()/max_volt
    # To do: play around with normalization
    button1 *= (button1*300)
    button2 *= (button2*300)
    return np.matmul(rot_mat, [(button2)-cm_to_pixel(1), (button1)-cm_to_pixel(1)])


def update_pos(pos, circ):
    circ.pos = pos
    circ.draw()


def is_home(circ, rad=37.795275591):  # default is 1 cm
    return circ.pos[0] < rad/2 and circ.pos[0] > -rad/2 and circ.pos[1] < rad/2 and circ.pos[1] > -rad/2


def calc_target_pos(angle, amp=8):
    magnitude = cm_to_pixel(amp)
    x = np.cos(angle*(np.pi/180)) * magnitude * -1
    y = np.sin(angle*(np.pi/180)) * magnitude
    return(x, y)


def calc_amplitude(pos):
    amp = np.sqrt(np.dot(pos, pos))
    return amp


# define rotation matrix for integrated cursor
rot_mat = [[np.cos(np.pi/4), -np.cos(np.pi/4)],
           [np.sin(np.pi/4), np.cos(np.pi/4)]]

# ---------- Main Experiment Run -----------------------------------------------------------------------------
# Create your Phidget channels
ch0 = config_channel(0, 100)
ch1 = config_channel(1, 100)

# Do stuff with your Phidgets here or in your event handlers.
mywin = visual.Window([1200, 800], monitor='testMonitor', units='pix')


int_cursor = visual.Circle(
    mywin, radius=cm_to_pixel(cursor_size), fillColor='green')  # integrated pos
target = visual.Circle(
    mywin, radius=cm_to_pixel(target_size), fillColor='blue')  # initial target
home = visual.Circle(
    mywin, radius=cm_to_pixel(home_size), lineColor='red')

while True:
    update_pos(get_pos(ch0, ch1, rot_mat), int_cursor)
    mywin.flip()
    home.draw()
    print(str(round(int_cursor.pos[0])) + ' ' + str(round(int_cursor.pos[0])
                                                    ) + ' + ' + str(round(home.pos[0])) + ' ' + str(round(home.pos[1])))

    # stop if button press
    if len(event.getKeys()) > 0:
        break
    event.clearEvents()


# Close the channels once the program is done.
ch0.close()
ch1.close()
