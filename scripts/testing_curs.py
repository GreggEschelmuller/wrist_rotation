from psychopy import visual, core, event
import numpy as np
import pandas as pd
import custom_functions as cf
import pickle
from datetime import datetime
import copy
import matplotlib.pyplot as plt

cursor_size = 0.1
# Creates window
win = visual.Window(fullscr=True, monitor='testMonitor',
                    units='pix', color='black', waitBlanking=False, screen=1, size=[1920, 1080])

# Create your NI channels
task = cf.config_channel(0, 1, 100)
# 0 deg rotation matrix
no_rot = cf.make_rot_mat(0)

# set up stimuli
int_cursor = visual.Circle(
    win, radius=cf.cm_to_pixel(cursor_size), fillColor='white')  # integrated pos
x_data = []
y_data = []

new_clock = core.Clock()
new_clock.reset()
print("Starting Collection")
while new_clock.getTime() <= 5:
    current_pos = cf.get_pos(task)
    x_data.append(current_pos[0])
    y_data.append(current_pos[1])
    #print("Ch1: " + str(round(current_pos[0], 2)) + "    Ch2: " + str(round(current_pos[1], 2)))
    cf.update_pos(current_pos, int_cursor, no_rot)
    win.flip()

task.stop()
task.close()

# plt.subplot(1,2,1)
# plt.plot(y_data)
# plt.subplot(1,2,2)
# plt.plot(x_data)
# plt.show()