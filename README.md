# pico_qwiic_addon
A repo for the Raspberry Pi Pico and Pico W, qwiic and reset button add-on, sample code and projects.

# circuitpython i2c code
```circuitpython
import board
from time import sleep
import busio

i2c = busio.I2C(board.GP27, board.GP26)
