import numpy as np
import pandas as pd
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *


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
    button1 *= 550
    button2 *= 550
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
