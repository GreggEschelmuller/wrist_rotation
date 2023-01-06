from psychopy import visual, core, event
import numpy as np
import pandas as pd
import custom_functions as cf
import pickle
from datetime import datetime
import copy
import matplotlib.pyplot as plt
import nidaqmx

cursor_size = 0.1
# Creates window
win = visual.Window(fullscr=True, monitor='testMonitor',
                    units='pix', color='black', waitBlanking=False, screen=1, size=[1920, 1080])

# Create your NI channels
#task = cf.config_channel(0, 1, 1000)

ch_num0 = 0
ch_num1 = 1
fs = 500

task = nidaqmx.Task()

task.ai_channels.add_ai_voltage_chan("Dev1/ai" + str(ch_num0), min_val=0, max_val=5)
task.ai_channels.add_ai_voltage_chan("Dev1/ai" + str(ch_num1), min_val=0, max_val=5)
task.timing.cfg_samp_clk_timing(fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
task.start()
# 0 deg rotation matrix
no_rot = cf.make_rot_mat(0)

# set up stimuli
int_cursor = visual.Circle(
    win, radius=cf.cm_to_pixel(cursor_size), fillColor='white')  # integrated pos

core.wait(0.2)

x_data = []
y_data = []
counter = 0
t0 = []
t1 = []
t2 = []

new_clock = core.Clock()
new_clock.reset()
print("Starting Collection")
while new_clock.getTime() <= 1:
    t0.append(core.getTime())
    current_pos = cf.get_pos(task)
    # x_data.append(x)
    # y_data.append(y)
    #print("Ch1: " + str(round(current_pos[0], 2)) + "    Ch2: " + str(round(current_pos[1], 2)))
    cf.update_pos([current_pos[0], current_pos[1]], int_cursor, no_rot)
    counter += 1
    t1.append(core.getTime())
    win.flip(clearBuffer=True)
    t2.append(core.getTime())

task.stop()
task.close()
print(counter)
draw_diff = [t1[i]-t0[i] for i in range(min(len(t0), len(t1)))]
flip_diff = [t2[i]-t1[i] for i in range(min(len(t0), len(t1)))]
print(np.mean(draw_diff))
print(np.mean(flip_diff))

# plt.subplot(1,2,1)
# plt.plot(y_data)
# plt.subplot(1,2,2)
# plt.plot(x_data)
# plt.show()