# μPython code for small robot

## Configuration

Copy `config.py.example` to `config.py`, then (re-)flash the robot
(see below).

## Flashing setup

In a Python 3 virtual env, do:

```console
$ python -m pip install esptool adafruit-ampy requests click
```

On Ubuntu install:

```bash
sudo apt-get install python3-pip python3-requests python3-click
pip3 install esptool adafruit-ampy ampy
```

Then, run `python flash-me.py mqtt` to flash the robot.

This uploads both firmware and Python modules.
If the firmware is successfully flashed, then on subsequent `flash-me.py`
you can pass `-X` to only update the Python modules.

## Diagnostics (MQTT)

 * robot moves both wheels after successfull connection to WiFi

 * otherwise open terminal and connect to the board

## hardware needed

 * NodeMCU board with ESP8266
 
 * DOIT Motor shield for NodeMCU [(guide)](https://cdn.hackaday.io/files/8856378895104/user-mannual-for-esp-12e-motor-shield.pdf)
 
 * Two DC motors with wheels
 
 * lunch box
 
## HOW TO: connect to terminal

 * Open terminal (Putty, Picocom, Minicom or whatever). speed: 115200

```bash
minicom -D /dev/ttyUSB0
```

 * Press `Ctrl+C` to stop running Python code. Prompt `>>>` should appear.

## Links

 Web joystick for MQTT is available at https://github.com/VerosK/mqtt-robot-webdriver/
