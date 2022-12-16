"""
This file contains a series of functions used for a wrist-based cursor control experiment.
The experiment is coded in psychopy. The functions and code were written by Gregg Eschelmuller.
"""

import numpy as np
import pandas as pd
from Phidget22.Devices.VoltageInput import *
import psychopy.core as core
import psychopy.event as event


# 24 inch diag - resololution 1920x1080
# PPI = diagnol in inches
def cm_to_pixel(cm):
    return cm * 91.79


def pixel_to_cm(pix):
    return pix/91.79


def read_trial_data(file_name, sheet=0):
    # Reads in the trial data from the excel file
    return pd.read_excel(file_name, sheet_name=sheet, engine='openpyxl')


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch

def make_rot_mat(theta):
    # Makes a rotation matrix for the integrated cursor
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])

def get_pos(ch0, ch1):
    chan1 = (5 - ch0.getVoltage() - 2.4)
    chan2 = (ch1.getVoltage() - 2.2)
    # To do: play around with normalization
    chan1 *= 550
    chan2 *= 550
    return chan1, chan2


def update_pos(pos, circ, rot_mat=make_rot_mat(0)):
    circ.pos = np.matmul(rot_mat, pos)
    circ.draw()


def calc_target_pos(angle, amp=8):
    # Calculates the target position based on the angle and amplitude
    magnitude = cm_to_pixel(amp)
    x = np.cos(angle*(np.pi/180)) * magnitude
    y = np.sin(angle*(np.pi/180)) * magnitude
    return x, y


def calc_amplitude(pos):
    # Calculates the amplitude of the cursor
    amp = np.sqrt(np.dot(pos, pos))
    return amp


# define rotation matrix for integrated cursor
def make_rot_mat(theta):
    # Makes a rotation matrix for the integrated cursor
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


def check_home_range(ch0, ch1, rot_mat, int_cursor, home_range, home, win):
    in_range = False
    while not in_range:
        if home_range.contains(get_pos(ch0, ch1)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            win.flip()
        current_pos = get_pos(ch0, ch1)
        update_pos(current_pos, int_cursor, rot_mat)
        home.draw()
        win.flip()
        


def check_home(int_cursor, home, ch0, ch1, rot_mat, home_clock, win):
    is_home = False
    while not is_home:
        if home.contains(get_pos(ch0, ch1)):
            home_clock.reset()
            while True:
                current_pos = get_pos(ch0, ch1)
                home.draw()
                update_pos(current_pos, int_cursor, rot_mat)
                win.flip()
                
                if home_clock.getTime() > 0.5:
                    is_home = True
                    break
                if not home.contains(get_pos(ch0, ch1)):
                    break
        current_pos = get_pos(ch0, ch1)
        home.draw()
        update_pos(current_pos, int_cursor, rot_mat)
        win.flip()
        

def save_trial_data(data_dict, move_clock, current_pos, int_cursor, condition, t_num):
    data_dict['Move_Times'].append(move_clock.getTime())
    data_dict['Wrist_x_end'].append(current_pos[0])
    data_dict['Wrist_y_end'].append(current_pos[1])
    data_dict['Curs_x_end'].append(int_cursor.pos[0])
    data_dict['Curs_y_end'].append(int_cursor.pos[1])
    data_dict['Target_pos'].append(condition.target_pos[t_num])
    data_dict['Rotation'].append(condition.rotation[t_num])
    data_dict['End_Angles'].append(np.degrees(np.arctan2(int_cursor.pos[1], int_cursor.pos[0])))
    return data_dict

def save_position_data(data_dict, int_cursor, current_pos, move_clock):
    data_dict['Curs_x_pos'] = int_cursor.pos[0]
    data_dict['Curs_y_pos'] = int_cursor.pos[1]
    data_dict['Wrist_x_pos'] = current_pos[0]
    data_dict['Wrist_y_pos'] = current_pos[1]
    data_dict['Time'] = move_clock.getTime()
    return data_dict


def run_trial(ch0, ch1, int_cursor, home, win, move_clock, rot_mat, target, end_data, trial_data, condition, t_num, feedback, trial_dict):
    timeLimit = 3
    current_trial = copy.deepcopy(trial_dict)
    # Waits to continue until cursor leaves home position
    while home.contains(get_pos(ch0, ch1)):
        current_pos = get_pos(ch0, ch1)
        home.draw()
        update_pos(current_pos, int_cursor, rot_mat)
        target.draw()
        win.flip()
        
        continue

    if not feedback:
        int_cursor.color = 'black'

    # run trial until time limit is reached or target is reached
    move_clock.reset()
    # Save wrist and cursor position data for whole trial
    while move_clock.getTime() <= timeLimit:
        # Run trial
        current_pos = get_pos(ch0, ch1)
        update_pos(current_pos, int_cursor, rot_mat)
        target.draw()
        win.flip()
        trial_data = save_position_data(trial_data, int_cursor, current_pos, move_clock)
        current_trial = save_position_data(current_trial, int_cursor, current_pos, move_clock)
        core.wait(1/1000, hogCPUperiod=1/1000) # waits for 1 ms. This is to avoid storing huge amounts of data, but will not effect cursor movement - may have to play around with
        

        if calc_amplitude(current_pos) > cm_to_pixel(condition.target_amp[t_num]):
            # Append trial data to storage variables
            end_data = save_trial_data(end_data, move_clock, current_pos, int_cursor, condition, t_num)
            current_trial = save_trial_data(current_trial, move_clock, current_pos, int_cursor, condition, t_num)
            break
    
    return trial_data, end_data, current_trial