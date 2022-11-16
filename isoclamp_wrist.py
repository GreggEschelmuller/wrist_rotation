from psychopy import visual, core, event
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------To Do: ------------------
# 1. make proper calibration
# 2. make cursor disappear after trial and reappear only when close to home
# 3. make excel file with parameters and read it in
# 4. Make practice in excel file
# 5. Set up window flip to not wait for screen flip
# ------------------------ Function and constant var set up ---------------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
timeLimit = 3
max_volt = 5
gain = 550


def cm_to_pixel(cm):
    return cm * 37.795275591


def pixel_to_cm(pix):
    return pix/37.795275591


def read_trial_data(file_name, sheet=0):
    # Reads in the trial data from the excel file
    return pd.read_excel(file_name, sheet_name=sheet, engine='openpyxl')


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


def get_pos(ch0, ch1, rot_mat):
    button1 = (5 - ch0.getVoltage() - 2.4)
    button2 = (ch1.getVoltage() - 2.2)
    # To do: play around with normalization
    button1 *= gain
    button2 *= gain
    # return [button1, button2]
    return (np.matmul(rot_mat, [button1, button2]))


def update_pos(pos, circ):
    circ.pos = pos
    circ.draw()


def calc_target_pos(angle, amp=8):
    # Calculates the target position based on the angle and amplitude
    # To do: make work properly
    magnitude = cm_to_pixel(amp)
    x = np.cos(angle*(np.pi/180)) * magnitude
    y = np.sin(angle*(np.pi/180)) * magnitude
    return(x, y)


def calc_amplitude(pos):
    # Calculates the amplitude of the cursor
    amp = np.sqrt(np.dot(pos, pos))
    return amp


# define rotation matrix for integrated cursor

def make_rot_mat(theta):
    # Makes a rotation matrix for the integrated cursor
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


no_rot = make_rot_mat(0)

rot_mat_flipx = [[-1, 0], [0, 1]]

rot_mat_flipy = [[1, 0], [0, -1]]

# ---------- Main Experiment Run ------------------------------------
# read data from xls file

ch0 = config_channel(2, 100)
ch1 = config_channel(1, 100)
trials = read_trial_data('Trials.xlsx', 0)

# Creates window
mywin = visual.Window(fullscr=True, monitor='testMonitor',
                      units='pix', color='black')


int_cursor = visual.Circle(mywin, radius=cm_to_pixel(
    cursor_size), fillColor='white')  # integrated pos

# Set up variables for data collection
end_angles = []
final_positions = []
move_times = []
# set up clock
move_clock = core.Clock()

# start trial loop
for i in range(len(trials.trial_num)):
    rot_mat = make_rot_mat(np.radians(trials.rotation[i]))
    int_cursor = visual.Circle(
        mywin, radius=cm_to_pixel(cursor_size), fillColor='white')  # integrated pos
    target = visual.Circle(
        mywin, radius=cm_to_pixel(target_size), fillColor='green')  # initial target
    home = visual.Circle(
        mywin, radius=cm_to_pixel(home_size), lineColor='red')  # home position

    # checks if cursor is in home position
    is_home = False
    while is_home == False:
        if home.contains(get_pos(ch0, ch1, no_rot)):
            is_home = True
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home.draw()
        mywin.flip()

    # Sets up target position
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
            move_times.append(move_clock.getTime())
            final_positions.append(current_pos)
            break

    mywin.flip()

# ------ Analysis and Saving--------------------
# To do:
# 1. Add additional data in output df

# Writes output data to dataframe and saves as excel
output_data = pd.DataFrame()
output_data['final_positions'] = final_positions
output_data['final_angles'] = [np.degrees((np.arctan2(final_positions[i][1], final_positions[i][0])))
                               for i in range(len(final_positions))]
output_data['target_positions'] = trials.target_pos
output_data['error'] = output_data['target_positions'] - \
    output_data['final_angles']
output_data['move_times'] = move_times
output_data['rotation'] = trials.rotation

output_data.to_excel('testing_output_data.xlsx')
