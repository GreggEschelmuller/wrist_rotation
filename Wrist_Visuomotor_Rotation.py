from psychopy import visual, core, event
import numpy as np
import pandas as pd
import custom_functions as cf
import pickle
from datetime import datetime


# ------------------To Do: ------------------



# ------------------------ Participant and file path --------------------------
print('Setting everything up...')
participant = 1
file_path = "Data/P" + str(participant) + "/participant_" + str(participant)
current_date = datetime.now()
study_info =  {
    "Participant": participant,
    "Date_Time": current_date,
    "Study ID": "Rotation"
}

# ------------------------ constant var set up --------------------------------

cursor_size = 0.2
target_size = 0.3
home_size = 0.3
home_range = home_size * 10.0
timeLimit = 3
max_volt = 5
gain = 550


# 0 deg rotation matrix
no_rot = cf.make_rot_mat(0)

# ---------- Main Experiment Run ------------------------------------

# Create your Phidget channels
ch0 = cf.config_channel(2, 100)
ch1 = cf.config_channel(1, 100)

# Read data from xls file
practice = cf.read_trial_data('Trials.xlsx', 'Practice')
baseline = cf.read_trial_data("Trials.xlsx", "Baseline")
exposure = cf.read_trial_data('Trials.xlsx', 'Trials')
post = cf.read_trial_data('Trials.xlsx', 'Post')


# Creates window
win = visual.Window(fullscr=True, monitor='testMonitor',
                      units='pix', color='black', waitBlanking=False)

# Create dictionaries to store data
position_data_template = {
    "Curs_y_pos": [],
    "Curs_x_pos": [],
    "Wrist_x_pos": [],
    "Wrist_y_pos": [],
    "Time": [],
}

template_data_dict = {
    "End_Angles": [],
    "Curs_x_pos": [],
    "Curs_y_pos": [],
    "Wrist_x_pos": [],
    "Wrist_y_pos": [],
    "Move_Times": [],
    "Target_pos": [],
    "Rotation": [],
    "Error": [],
}

# Summary end point data dictionaries
practice_end_data = template_data_dict.copy()
baseline_end_data = template_data_dict.copy()
exposure_end_data = template_data_dict.copy()
post_end_data = template_data_dict.copy()

# Continuous data per trial data dictionaries
practice_trial_data = position_data_template.copy()
baseline_trial_data = position_data_template.copy()
exposure_trial_data = position_data_template.copy()
post_trial_data = position_data_template.copy()


# set up clock
move_clock = core.Clock()
home_clock = core.Clock()

# set up stimuli
home = visual.Circle(
    win, radius=cf.cm_to_pixel(home_size), lineColor='red')  # home position
home_range = visual.Circle(
    win, radius=cf.cm_to_pixel(home_range), lineColor='black')  # home range position
int_cursor = visual.Circle(    
    win, radius=cf.cm_to_pixel(cursor_size), fillColor='black')  # integrated pos
target = visual.Circle(
    win, radius=cf.cm_to_pixel(target_size), fillColor='green')  # initial target

print('Done set up')

# -------------- start practice trial loop ------------------------------------

for i in range(len(practice.trial_num)):
    rot_mat = cf.make_rot_mat(np.radians(practice.rotation[i]))
    home.draw()
    int_cursor.color = 'black'
    int_cursor.draw()
    win.flip()

    # Checks if cursor is close to home and turns cursor white
    cf.check_home_range(ch0, ch1, no_rot, int_cursor, home_range, home, win)

    # checks if cursor is in home position
    cf.check_home(int_cursor, home, ch0, ch1, no_rot, home_clock, win)

    # Sets up target position
    current_target_pos = cf.calc_target_pos(
        practice.target_pos[i], practice.target_amp[i])
    cf.update_pos(current_target_pos, target, no_rot)
    win.flip()

    # Run trial
    practice_trial_data, practice_end_data = cf.run_trial(ch0, ch1, int_cursor, home, win, move_clock, rot_mat, target, practice_end_data, practice_trial_data, practice, i, True)
    
    # Leave current window for 200ms
    core.wait(0.2, hogCPUperiod=0.2)
    cf.check_esc(win)
    win.flip()
    
print('Saving Practice Data')
# Save dict to excel as a backup
practice_output = pd.DataFrame.from_dict(practice_end_data)
practice_output.to_excel(file_path + "_practice.xlsx")
# Save dict to pickel
with open(file_path + '_practice.pkl', 'wb') as f:
    pickle.dump(practice_end_data, f)
print('Practice Data Saved')

# -------------- start baseline trial loop ---------------------------------------------
for i in range(len(baseline.trial_num)):
    rot_mat = cf.make_rot_mat(np.radians(baseline.rotation[i]))
    home.draw()
    int_cursor.color = 'black'
    int_cursor.draw()
    win.flip()

    # Checks if cursor is close to home and turns cursor white
    cf.check_home_range(ch0, ch1, no_rot, int_cursor, home_range, home, win)

    # checks if cursor is in home position
    cf.check_home(int_cursor, home, ch0, ch1, no_rot, home_clock, win)

    # Sets up target position
    current_target_pos = cf.calc_target_pos(
        baseline.target_pos[i], baseline.target_amp[i])
    cf.update_pos(current_target_pos, target, no_rot)
    win.flip()
    
    # Run trial
    baseline_trial_data, baseline_end_data = cf.run_trial(ch0, ch1, int_cursor, home, win, move_clock, rot_mat, target, baseline_end_data, baseline_trial_data, baseline, i, False)
    
    # Leave current window for 200ms
    core.wait(0.2, hogCPUperiod=0.2)
    cf.check_esc(win)
    win.flip()
    
print('Saving Baseline Data')
# Save dict to excel as a backup
baseline_output = pd.DataFrame.from_dict(baseline_end_data)
baseline_output.to_excel(file_path + "_baseline.xlsx")
# Save dict to pickel
with open(file_path + '_baseline.pkl', 'wb') as f:
    pickle.dump(baseline_end_data, f)
print('Baseline Data Saved')

# -------------------- start experimental trial loop -----------------------------------
for i in range(len(exposure.trial_num)):
    rot_mat = cf.make_rot_mat(np.radians(exposure.rotation[i]))
    home.draw()
    int_cursor.color = 'black'
    int_cursor.draw()
    win.flip()

    # Checks if cursor is close to home and turns cursor white
    cf.check_home_range(ch0, ch1, no_rot, int_cursor, home_range, home, win)

    # checks if cursor is in home position
    cf.check_home(int_cursor, home, ch0, ch1, no_rot, home_clock, win)

    # Sets up target position
    current_target_pos = cf.calc_target_pos(
        exposure.target_pos[i], exposure.target_amp[i])
    cf.update_pos(current_target_pos, target, no_rot)
    win.flip()
    # Run trial
    exposure_trial_data, exposure_end_data = cf.run_trial(ch0, ch1, int_cursor, home, win, move_clock, rot_mat, target, exposure_end_data, exposure_trial_data, baseline, i, True)
    
    # Leave current window for 200ms
    core.wait(0.2, hogCPUperiod=0.2)
    cf.check_esc(win)
    win.flip()

print('Saving Exposure Data')
# Save dict to excel as a backup
exposure_output = pd.DataFrame.from_dict(exposure_end_data)
exposure_output.to_excel(file_path + "_exposure.xlsx")
# Save dict to pickel
with open(file_path + '_exposure.pkl', 'wb') as f:
    pickle.dump(exposure_end_data, f)
print('Exposure Data Saved')

# -------------- start post trial loop ---------------------------------------------
for i in range(len(post.trial_num)):
    rot_mat = cf.make_rot_mat(np.radians(post.rotation[i]))
    home.draw()
    int_cursor.color = 'black'
    int_cursor.draw()
    win.flip()

    # Checks if cursor is close to home and turns cursor white
    cf.check_home_range(ch0, ch1, no_rot, int_cursor, home_range, home, win)

    # checks if cursor is in home position
    cf.check_home(int_cursor, home, ch0, ch1, no_rot, home_clock, win)

    # Sets up target position
    current_target_pos = cf.calc_target_pos(
        post.target_pos[i], post.target_amp[i])
    cf.update_pos(current_target_pos, target, no_rot)
    win.flip()
    # Run trial
    post_trial_data, post_end_data = cf.run_trial(ch0, ch1, int_cursor, home, win, move_clock, rot_mat, target, post_end_data, post_trial_data, baseline, i, False)
    
    # Leave current window for 200ms
    core.wait(0.2, hogCPUperiod=0.2)
    cf.check_esc(win)
    win.flip()
    
print('Saving Post Data')
# Save dict to excel as a backup
post_output = pd.DataFrame.from_dict(post_end_data)
post_output.to_excel(file_path + "_post.xlsx")
# Save dict to pickel
with open(file_path + '_post.pkl', 'wb') as f:
    pickle.dump(post_end_data, f)
print('Post Data Saved')


ch0.close()
ch1.close()
# ------ Analysis and Saving-----------------------------------------------------------------
print("Saving all data")
all_data = {"Practice_Summary": practice_end_data,
            "Practice_Movements": practice_trial_data,
            "Baseline_Summary": baseline_end_data,
            "Baseline_Movements": baseline_trial_data,
            "Exposure_Summary": exposure_end_data,
            "Exposure_Movements": exposure_trial_data,
            "Post_Summary": post_end_data,
            "Post_Movements": post_trial_data,
            "Study Info": study_info}

with open(file_path + '_all.pkl', 'wb') as f:
    pickle.dump(all_data, f)

print("Add data saved, experiment over")
