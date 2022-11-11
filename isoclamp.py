
from psychopy import visual, core, event
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------ Function and constant var set up ---------------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
timeLimit = 3
max_volt = 5
gain = 250


def cm_to_pixel(cm):
    return cm * 37.795275591


def pixel_to_cm(pix):
    return pix/37.795275591


def read_trial_data(file_name, sheet=0):
    return pd.read_excel(file_name, sheet_name=sheet, engine='openpyxl')


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setDeviceSerialNumber(678135)
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


def get_pos(ch0, ch1, rot_mat):
    button1 = (5-ch0.getVoltage() - 5/2)
    button2 = (5-ch1.getVoltage() - 5/2.5)
    # To do: play around with normalization
    button1 *= gain
    button2 *= gain
    # return [button1, button2]
    return np.matmul(rot_mat, [(button1), (button2)])


def update_pos(pos, circ):
    circ.pos = pos
    circ.draw()


def is_home(circ, rad):
    return (circ.pos[0] < rad/2 and circ.pos[0] > -rad/2 and circ.pos[1] < rad/2 and circ.pos[1] > -rad/2)


def calc_target_pos(angle, amp=8):
    magnitude = cm_to_pixel(amp)
    x = np.cos(angle*(np.pi/180)) * magnitude * -1
    y = np.sin(angle*(np.pi/180)) * magnitude
    return(x, y)


def calc_amplitude(pos):
    amp = np.sqrt(np.dot(pos, pos))
    return amp


def trial_counter(time=3):
    current_time = time
    for i in range(time):
        counter_stim = visual.TextStim(
            mywin, text=str(current_time), color='blue')
        counter_stim.draw()
        mywin.flip()
        core.wait(1)
        current_time -= 1


# define rotation matrix for integrated cursor
rot_mat = [[np.cos(np.pi/4), -np.sin(np.pi/4)],
           [np.sin(np.pi/4), np.cos(np.pi/4)]]

# ---------- Main Experiment Run ------------------------------------
# read data from xls file
trials = read_trial_data('Trials.xlsx', 0)
# Create your Phidget channels
ch0 = config_channel(1, 1000)
ch1 = config_channel(2, 1000)

# Creates window
mywin = visual.Window(fullscr=True, monitor='testMonitor',
                      units='pix', color='black')

int_cursor = visual.Circle(mywin, radius=cm_to_pixel(
    cursor_size), fillColor='white')  # integrated pos

keys = []
while len(keys) == 0:
    keys = event.getKeys()
    current_pos = get_pos(ch0, ch1, rot_mat)
    update_pos(current_pos, int_cursor)
    mywin.flip()


# Create stimuli
end_angles = []
final_positions = []
move_clock = core.Clock()

for i in range(len(trials.trial_num)):
    int_cursor = visual.Circle(
        mywin, radius=cm_to_pixel(cursor_size), fillColor='white')  # integrated pos
    target = visual.Circle(
        mywin, radius=cm_to_pixel(target_size), fillColor='red')  # initial target
    home = visual.Circle(
        mywin, radius=cm_to_pixel(home_size), lineColor='red')
    trial_counter(3)

    target.fillColor = 'green'
    update_pos(calc_target_pos(
        trials.target_pos[i], trials.target_amp[i]), target)
    mywin.flip()

    move_clock.reset()
    while move_clock.getTime() <= timeLimit:
        # Run trial
        current_pos = get_pos(ch0, ch1, rot_mat)
        update_pos(current_pos, int_cursor)
        update_pos(calc_target_pos(
            trials.target_pos[i], trials.target_amp[i]), target)
        mywin.flip()

        if calc_amplitude(current_pos) > cm_to_pixel(trials.target_amp[i]):
            move_time = move_clock.getTime()
            final_positions.append(current_pos)
            break

    mywin.flip()

# Close the channels once the program is done.
ch0.close()
ch1.close()

# ------ Analysis and Saving--------------------
# To do: update output data to include all trial data
# Merge input df with output df
# final_angles = [(np.arctan(final_positions[i][1]/final_positions[i][0])) * (180/np.pi)
#                 for i in range(len(final_positions))]
# output_data = pd.DataFrame()
# output_data['final_positions'] = final_positions
# output_data['final_angles'] = final_angles
# output_data['target_positions'] = trials.target_pos
# output_data['error'] = output_data['target_positions'] - \
#     output_data['final_angles']

# output_data.to_csv('testing_output_data.csv')
