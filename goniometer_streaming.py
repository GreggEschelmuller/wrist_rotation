from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time


def onVoltageRatioChange(self, voltageRatio):
    print("VoltageRatio: " + str(voltageRatio*1000))


def main():
    voltageRatioInput2 = VoltageRatioInput()

    voltageRatioInput2.setChannel(2)

    voltageRatioInput2.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

    voltageRatioInput2.openWaitForAttachment(5000)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    voltageRatioInput2.close()


main()
