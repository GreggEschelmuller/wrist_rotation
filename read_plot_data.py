from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.VoltageInput import *
import time
import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
from psychopy import core


def config_channel(ch_num, fs):
    ch = VoltageInput()
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


def config_bridge_channel(ch_num, fs):
    ch = VoltageRatioInput()
    ch.setChannel(ch_num)
    ch.openWaitForAttachment(1000)
    ch.setDataRate(fs)
    return ch


# For normal voltage input
ch0 = config_channel(2, 1000)

# For the bridge amplifier
# ch0 = config_bridge_channel(2, ch.getmaxDataRate())


pot = []

print('Starting Collection')
t_end = time.time()+5
while time.time() < t_end:
    voltage = ch0.getVoltage()
    # voltage = ch0.getVoltageRatio()
    pot = np.append(pot, voltage)

ch0.close()
print('Done Collection')
print(len(pot))
fig, ax = plt.subplots()
ax.plot(pot)
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='Pot Data')
ax.grid()
plt.show()

#data_file = {'Voltage': pot, "label": "Condition"}
#savemat("../kin500a.mat", data_file)
