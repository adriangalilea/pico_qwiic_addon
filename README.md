# Pico QwiicReset Addon
Plug, Reset, and Prototype Effortlessly.


https://github.com/adriangalilea/pico_qwiic_addon/assets/90320947/8367507b-55c4-4f87-a407-c8dec5c27a95


Available [here](https://www.duppa.net/shop/rpi-pico-reset-button-qwiic-connector/)

## Pico Pain Points
1. **Flash Mode**: Requires unplugging and holding BOOTSEL while you plug.
2. **Board Hangs**: Requires unplugging and plugging back in to reset.
3. **Prototyping**: Absence of a Qwiic/Stemma QT connector for easy module connection without soldering.

## 1.50€ Pico QwiicReset Addon Solution
Meet your new best friend for faster prototyping and smoother iterations. This cute little guy is packed with features you didn't know you needed but won't be able to live without:
- **Instant Reset**: A single button press does the trick.
- **Flash Mode**: Just press both buttons simultaneously.
- **Compact design**: No added bulk—just more functionality packed into your existing Pico setup.
- **Plug-and-Play Prototyping**: Equipped with a Qwiic/Stemma QT connector, say goodbye to soldering and hello to an expansive ecosystem of modules.

circuitpython i2c code
```circuitpython
import board
import busio

i2c = busio.I2C(board.GP27, board.GP26)
```

The ultimate add-on to turbocharge your Raspberry Pi Pico (and Pico W!) experience.

# Installation
Place it in the right spot:

![image](https://github.com/adriangalilea/pico_qwiic_addon/assets/90320947/3c39b017-19d3-4dff-a257-d158bc8747f9)

Solder
- **With pins**
![IMG_2428](https://github.com/adriangalilea/pico_qwiic_addon/assets/90320947/dd74b585-b882-4d4b-8c6a-648e3f6db83c)

- **Without pins**
![IMG_2491](https://github.com/adriangalilea/pico_qwiic_addon/assets/90320947/621e9f45-daf0-4ff9-8bf1-081d0815dfab)

## Compatibility
- **Fully Compatible**: Works seamlessly with the Pico and Pico W.
- **Not Compatible**: Cannot be used with the Pico WH due to interference with the debug connector.
