from Facedancer import *
from MAXUSBApp import *
from KeyboardEMU import *
from GoodFETMAXUSB import *

modifiers = {'None': 0b00000000,
             'LeftCtrl': 0b00000001,
             'LeftShift': 0b00000010,
             'LeftAlt': 0b00000100,
             'LeftGUI': 0b00001000,
             'RightCtrl': 0b00010000,
             'RightShift': 0b00100000,
             'RightAlt': 0b01000000,
             'RightGUI': 0b10000000
            }

class KeyboardController():
    def __init__(self):
        self.interface = USBKeyboardInterface()
        #self.device = USBKeyboardDevice(MAXUSBApp(Facedancer(GoodFETSerialPort(), verbose=1), verbose=1), verbose=4)

    def type_string(self,string,*args):
        """
        Handle string
        :param string: string to send
        :param args: modifiers as defined by the strings in modifiers dict.
        :return:
        """
        self.interface = USBKeyboardInterface()
        hid_arr = []
        modifier = 0x00

        for key in args:
            modifier = modifier | modifiers[key]
        for letter in string:
            m,k = GoodFETMAXUSBHID().asc2hid(letter)
            if letter.isupper():
                hid_arr.append(hex(k) | modifiers['LeftShift'])
            else:
                hid_arr.append(hex(k))
            hid_arr.append(0x00)
        self.interface.text = hid_arr
        self.interface.usr_modifiers =  modifier
        self.send_HID()

    def send_HID(self):
        sp = GoodFETSerialPort()
        fd = Facedancer(sp, verbose=1)
        u = MAXUSBApp(fd, verbose=1)

        device = USBKeyboardDevice(u, self.interface, verbose=4)
        device.connect()
        try:
            device.run()
        except KeyboardInterrupt:
            device.disconnect()







m,k = GoodFETMAXUSBHID().asc2hid('a')
print k
print type(k)


# sp = GoodFETSerialPort()
# fd = Facedancer(sp, verbose=1)
# u = MAXUSBApp(fd, verbose=1)
#
# d = USBKeyboardDevice(u, verbose=4)
#
# d.connect()
#
# try:
#
#     d.run()
# # SIGINT raises KeyboardInterrupt
# except KeyboardInterrupt:
#     d.disconnect()
