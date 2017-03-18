#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Driver for the Si7021 humidity and temperature sensor.
"""

class Si7021:
    """ Driver for the Si7021 humidity and temperature sensor.

    Usage:
        sensor = Si7021(smbus.SMBus(1))
        print("%.1f %%RH, %.1f °C" % sensor.read())
        sensor.heater_mA = 50
        time.sleep(10)
        print("%.1f %%RH, %.1f °C" % sensor.read())
        sensor.heater_mA = 0
    """
    RH_NO_HOLD = 0xF5
    RH_HOLD = 0xE5
    LAST_TEMPERATURE = 0xE0

    READ_HEATER_CTRL = 0x11
    WRITE_HEATER_CTRL = 0x51

    READ_USR_REG = 0xE7
    WRITE_USR_REG = 0xE6

    RESET = 0xFE

    HEATER_OFFSET = 3.09
    HEATER_STEP = 6.074

    USR_RES1 = 128
    USR_VDDS = 64
    USR_HTRE = 4
    USR_RES0 = 1
    def __init__(self, bus):
        self.bus = bus
        self.addr = 0x40

    def reset(self):
        """ Reset the sensor """
        self.bus.write_byte(self.addr, self.RESET)

    def read(self):
        """ Read relative humidity and temperature.

        Returns a tuple (rh, temperature)
        """
        rh = self.bus.read_word_data(self.addr, self.RH_HOLD)
        t = self.bus.read_word_data(self.addr, self.LAST_TEMPERATURE)

        # Swap bytes
        rh = ((rh & 0xff) << 8) | (rh >> 8)
        t = ((t & 0xff) << 8) | (t >> 8)

        rh = 125. * rh  / 65536. - 6 # See DS 5.1.1
        rh = max(0, min(100, rh)) # See DS 5.1.1
        t = 175.72 * t / 65536. - 46.85 # See DS 5.1.2
        return (rh, t)

    @property
    def heater_mA(self):
        """ Get heater current in mA """
        usr = self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        if usr & self.USR_HTRE:
            value = self.bus.read_byte_data(self.addr, self.READ_HEATER_CTRL)
            value = value * self.HEATER_STEP + self.HEATER_OFFSET
            return value
        return 0

    @heater_mA.setter
    def heater_mA(self, value):
        """ Set heater current in mA.

        Turing on and off of the heater is handled automatically.
        """
        usr = self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        if not value:
            usr &= ~self.USR_HTRE
        else:
            # Enable heater and calculate settings
            setting = 0
            if value > self.HEATER_OFFSET:
                value -= self.HEATER_OFFSET
                setting = int(round(value / self.HEATER_STEP)) # See DS 5.5
                setting = min(15, setting) #Avoid overflow
            self.bus.write_byte_data(self.addr, self.WRITE_HEATER_CTRL, setting)
            usr |= self.USR_HTRE
        self.bus.write_byte_data(self.addr, self.WRITE_USR_REG, usr)

    def set_resultion(self, bits_rh):
        """ Select measurement resultion.

        bits_rh is the number of bits for the RH measurement. Number of
        bits for temperature is choosen accoring to the table in section 6.1
        of the datasheet.
        """
        usr = self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        usr &= ~(self.USR_RES0 | self.USR_RES1)
        if bits_rh == 8:
            usr |= self.USR_RES1
        elif bits_rh == 10:
            usr |= self.USR_RES1
        elif bits_rh == 11:
            usr |= self.USR_RES0 | self.USR_RES1
        elif bits_rh != 12:
            raise ValueError("Unsupported number of bits.")
        self.bus.write_byte_data(self.addr, self.WRITE_USR_REG, usr)


    # Reading the device ID seems to be impossible with the smbus functions
    # as they do not support 2 byte register adresses. And the Si7021 does
    # not accept the address in two transactions
