"""
This file contains a series of functions used for a wrist-based cursor control experiment.
The experiment is coded in psychopy. The functions and code were written by Gregg Eschelmuller.
"""

import numpy as np
import pandas as pd
from Phidget22.Devices.VoltageInput import *
import psychopy.core as core
import psychopy.event as event


def check_esc(win):
    keys = event.getKeys()
    if keys in keys[0] == 'Esc':
        win.close()
        core.quit()
    else:
        return None


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


def check_home_range(ch0, ch1, rot_mat, int_cursor, home_range, home, mywin):
    in_range = False
    while not in_range:
        if home_range.contains(get_pos(ch0, ch1)):
            in_range = True
            int_cursor.color = 'white'
            int_cursor.draw()
            mywin.flip()
        current_pos = get_pos(ch0, ch1)
        update_pos(current_pos, int_cursor, rot_mat)
        home.draw()
        mywin.flip()
        check_esc(mywin)


def check_home(int_cursor, home, ch0, ch1, rot_mat, home_clock, mywin):
    is_home = False
    while not is_home:
        if home.contains(get_pos(ch0, ch1)):
            home_clock.reset()
            while True:
                current_pos = get_pos(ch0, ch1)
                update_pos(current_pos, int_cursor, rot_mat)
                home.draw()
                mywin.flip()
                check_esc(mywin)
                if home_clock.getTime() > 0.5:
                    is_home = True
                    break
                if not home.contains(get_pos(ch0, ch1)):
                    break
        current_pos = get_pos(ch0, ch1)
        update_pos(current_pos, int_cursor, rot_mat)
        home.draw()
        mywin.flip()
        check_esc(mywin)

def save_trial_data(data_dict, move_clock, current_pos, int_cursor, condition, i):
    data_dict['Move_Times'].append(move_clock.getTime())
    data_dict['Wrist_x_pos'].append(current_pos[0])
    data_dict['Wrist_y_pos'].append(current_pos[1])
    data_dict['Curs_x_pos'].append(int_cursor.pos[0])
    data_dict['Curs_y_pos'].append(int_cursor.pos[1])
    data_dict['Target_pos'].append(condition.target_pos[i])
    data_dict['Rotation'].append(condition.rotation[i])
    data_dict['End_Angles'].append(np.degrees(np.arctan2(int_cursor.pos[1], int_cursor.pos[0])))
    data_dict['Error'].append(data_dict['Target_pos'][i] - data_dict['End_Angles'][i])
    return data_dict

def save_position_data(data_dict, int_cursor, current_pos, move_clock):
    data_dict['Curs_x_pos'] = int_cursor.pos[0]
    data_dict['Curs_y_pos'] = int_cursor.pos[1]
    data_dict['Wrist_x_pos'] = current_pos[0]
    data_dict['Wrist_y_pos'] = current_pos[1]
    data_dict['Time'] = move_clock.get_time()
    return data_dict