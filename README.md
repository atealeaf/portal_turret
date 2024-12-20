# Portal Turret

## Overview
This Portal Turret is a replica of the one from the video game *Portal*. It can respond to various stimuli through sensors and motors. This project uses a Raspberry Pi 4 Model B as the central processing unit, with firmware and software developed in Python to control the turret's movements and audio output.

## Website
More detailed information can be found at [this website](https://catmoonster17.github.io/pie-2024-03/portal-turret/software.html).

Long link: https://catmoonster17.github.io/pie-2024-03/portal-turret/software.html

## Features
- Control motors and servos.
- Respond to sound levels and IR remote control signals.
- Play audio and music based on sensor inputs.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/atealeaf/portal_turret.git
   cd portal_turret
   ```

2. **Install dependencies:**
  Make sure you have Python 3.7 or higher installed on your Raspberry Pi. Then, install the required libraries:
  ```bash
  pip install RPi.GPIO adafruit-circuitpython-lis2mdl adafruit-circuitpython-lsm303-accel adafruit-circuitpython-pcf8591 audioplayer mutagen playsound
  ```

3. **Install LIRC:**
   Follow the instructions on the [LIRC website](https://www.lirc.org/) to set up the IR remote control functionality.

4. **Run the software:**
  Execute the main program:
   ```bash
   python main.py
   ```
