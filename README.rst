Si7021
======

Driver for the Si7021 humidity and temperature sensor.

Dependencies
------------

* smbus-cffi (or some compatible library)

  See https://github.com/bivab/smbus-cffi/blob/master/README.rst for install instructions.

Installation
------------

1. pip install from PyPi
::

  pip install Si7021

2. pip install from git
::

  pip install git+https://github.com/herm/Si7021

3. Clone the repository and run setup.py
::

  git clone https://github.com/herm/Si7021
  python setup.py install

Usage
-----

If you have a sensor connected to I2C bus 1, you may run
::

  >>> from si7021 import Si7021
  >>> from time import sleep
  >>> from smbus import SMBus
  >>> sensor = Si7021(SMBus(1))
  >>> print("%.1f %%RH, %.1f °C" % sensor.read())
  >>> sensor.heater_mA = 50
  >>> sleep(10)
  >>> print("%.1f %%RH, %.1f °C" % sensor.read())
  >>> sensor.heater_mA = 0


Bug Reporting
-------------

To submit a bugreport use the GitHub bugtracker for the project:

  https://github.com/herm/Si7021/issues
