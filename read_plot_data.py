from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time
import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
from psychopy import core


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setDeviceSerialNumber(678135)
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


ch0 = config_channel(2, 1000)
pot = np.array([])

pot = []

print('Starting Collection')
t_end = time.time()+1
while time.time() < t_end:
    pot = np.append(pot, ch0.getVoltage())
    core.wait(0.01, hogCPUperiod=0.01)

ch0.close()
print('Done Collection')
print(len(pot))
fig, ax = plt.subplots()
ax.plot(pot)
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='Pot Data')
ax.grid()
plt.show()
print(len(pot))

#data_file = {'Voltage': pot, "label": "Condition"}
#savemat("../kin500a.mat", data_file)
