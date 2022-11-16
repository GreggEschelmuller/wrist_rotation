from psychopy import visual, core, event
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import numpy as np
import pandas as pd


# ------------------To Do: ------------------
# 1. make proper calibration
# 2. make cursor disappear after trial and reappear only when close to home - working on
# 3. make excel file with parameters and read it in
# 4. Make practice in excel file
# 5. Set up window flip to not wait for screen flip
# 6. Code function to run experimental block
# ------------------------ Function and constant var set up ---------------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
home_range = home_size * 10.0
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

practice = read_trial_data('Trials.xlsx', 'Practice')
baseline = read_trial_data("Trials.xlsx", "Baseline")
trials = read_trial_data('Trials.xlsx', 'Trials')
post = read_trial_data('Trials.xlsx', 'Post')


# Creates window
mywin = visual.Window(fullscr=True, monitor='testMonitor',
                      units='pix', color='black', waitBlanking=False)

# Set up variables for data collection
end_angles = []
final_positions = []
move_times = []
condition = []
# set up clock
move_clock = core.Clock()

# set up stimuli
home = visual.Circle(
    mywin, radius=cm_to_pixel(home_size), lineColor='red')  # home position
home_range = visual.Circle(
    mywin, radius=cm_to_pixel(home_range), lineColor='white', opacity=0.2)  # home position
int_cursor = visual.Circle(
    mywin, radius=cm_to_pixel(cursor_size), fillColor='black')  # integrated pos
target = visual.Circle(
    mywin, radius=cm_to_pixel(target_size), fillColor='green')  # initial target
practice_text = visual.TextStim(
    mywin, text='Practice - Full Feedback', pos=(0, 0), color='white', height=100)
baseline_text = visual.TextStim(
    mywin, text='Baseline - No Feedback', pos=(0, 0), color='white', height=100)
experiment_text = visual.TextStim(
    mywin, text='Experimental Trials', pos=(0, 0), color='white', height=100)
post_text = visual.TextStim(
    mywin, text='Post - No Feedback', pos=(0, 0), color='white', height=100)

# -------------- start practice trial loop ---------------------------------------------
practice_text.draw()
mywin.flip()
core.wait(2)
for i in range(len(practice.trial_num)):
    rot_mat = make_rot_mat(np.radians(practice.rotation[i]))
    home_range.draw()
    home.draw()
    # If cursor is in range, color circle white
    in_range = False
    while in_range == False:
        if home_range.contains(get_pos(ch0, ch1, no_rot)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            mywin.flip()
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home_range.draw()
        home.draw()
        mywin.flip()

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
        practice.target_pos[i], practice.target_amp[i]), target)
    mywin.flip()

    move_clock.reset()
    while move_clock.getTime() <= timeLimit:
        # Run trial
        current_pos = get_pos(ch0, ch1, rot_mat)
        update_pos(current_pos, int_cursor)
        update_pos(calc_target_pos(
            practice.target_pos[i], practice.target_amp[i]), target)
        mywin.flip()

        if calc_amplitude(current_pos) > cm_to_pixel(practice.target_amp[i]):
            move_times.append(move_clock.getTime())
            final_positions.append(current_pos)
            update_pos(current_pos, int_cursor)
            condition.append('Practice')
            core.wait(0.2, hogCPUperiod=0.2)
            break

    mywin.flip()

# -------------- start baseline trial loop ---------------------------------------------
baseline_text.draw()
mywin.flip()
core.wait(2)
for i in range(len(baseline.trial_num)):
    rot_mat = make_rot_mat(np.radians(baseline.rotation[i]))
    home_range.draw()
    home.draw()
    # If cursor is in range, color circle white
    in_range = False
    while in_range == False:
        if home_range.contains(get_pos(ch0, ch1, no_rot)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            mywin.flip()
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home_range.draw()
        home.draw()
        mywin.flip()

    # checks if cursor is in home position
    is_home = False
    while is_home == False:
        if home.contains(get_pos(ch0, ch1, no_rot)):
            is_home = True
            int_cursor.color = 'black'
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home.draw()
        mywin.flip()

    # Sets up target position
    update_pos(calc_target_pos(
        baseline.target_pos[i], baseline.target_amp[i]), target)
    mywin.flip()

    move_clock.reset()
    while move_clock.getTime() <= timeLimit:
        # Run trial
        current_pos = get_pos(ch0, ch1, rot_mat)
        update_pos(current_pos, int_cursor)
        update_pos(calc_target_pos(
            baseline.target_pos[i], baseline.target_amp[i]), target)
        mywin.flip()

        if calc_amplitude(current_pos) > cm_to_pixel(baseline.target_amp[i]):
            move_times.append(move_clock.getTime())
            final_positions.append(current_pos)
            update_pos(current_pos, int_cursor)
            condition.append('Baseline')
            core.wait(0.2, hogCPUperiod=0.2)
            break

    mywin.flip()

# -------------------- start experimental trial loop -----------------------------------
experiment_text.draw()
mywin.flip()
core.wait(2)
for i in range(len(trials.trial_num)):
    rot_mat = make_rot_mat(np.radians(trials.rotation[i]))

    # If cursor is in range, color circle white
    in_range = False
    while in_range == False:
        if home_range.contains(get_pos(ch0, ch1, no_rot)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            mywin.flip()
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home_range.draw()
        home.draw()
        mywin.flip()

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
            update_pos(current_pos, int_cursor)
            condition.append('Trial')
            int_cursor.color = 'black'
            int_cursor.draw()
            mywin.flip()
            core.wait(0.2, hogCPUperiod=0.2)
            break

    mywin.flip()

# -------------- start post trial loop ---------------------------------------------
post_text.draw()
mywin.flip()
core.wait(2)
for i in range(len(post.trial_num)):
    rot_mat = make_rot_mat(np.radians(post.rotation[i]))

    # If cursor is in range, color circle white
    in_range = False
    while in_range == False:
        if home_range.contains(get_pos(ch0, ch1, no_rot)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            mywin.flip()
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home_range.draw()
        home.draw()
        mywin.flip()

    # checks if cursor is in home position
    is_home = False
    while is_home == False:
        if home.contains(get_pos(ch0, ch1, no_rot)):
            is_home = True
            int_cursor.color = 'black'
        current_pos = get_pos(ch0, ch1, no_rot)
        update_pos(current_pos, int_cursor)
        home.draw()
        mywin.flip()

    # Sets up target position
    update_pos(calc_target_pos(
        post.target_pos[i], post.target_amp[i]), target)
    mywin.flip()

    move_clock.reset()
    while move_clock.getTime() <= timeLimit:
        # Run trial
        current_pos = get_pos(ch0, ch1, rot_mat)
        update_pos(current_pos, int_cursor)
        update_pos(calc_target_pos(
            post.target_pos[i], post.target_amp[i]), target)
        mywin.flip()

        if calc_amplitude(current_pos) > cm_to_pixel(post.target_amp[i]):
            move_times.append(move_clock.getTime())
            final_positions.append(current_pos)
            update_pos(current_pos, int_cursor)
            condition.append('Post')
            core.wait(0.2, hogCPUperiod=0.2)
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
output_data['target_positions'] = [practice.target_pos,
                                   baseline.target_pos, trials.target_pos, post.target_pos]
output_data['error'] = output_data['target_positions'] - \
    output_data['final_angles']
output_data['move_times'] = move_times
output_data['rotation'] = trials.rotation
output_data['condition'] = condition

output_data.to_excel('testing_output_data.xlsx')
