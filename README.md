## DoomsDay Machine NeoPixel Light Code

This code is designed to run on Raspberry Pi Pico, in a MicroPython environment.  It was built for a model of the DoomsDay machine (from Star Trek original series TV show), which can be found here:

https://www.thingiverse.com/thing:6989169

<img width="515" alt="image" src="https://github.com/user-attachments/assets/01786ba0-4ee9-467e-8691-98aaf0b1a110" />

The code is written so that when ran in a MicroPython environment, it will use the MicroPython libraries instead of the mock libraries. 
If ran on a normal PC, mock libraries will be used that simulate the display.  This is helpful for testing and visualizing effects before installing them on the Pi Pico.

It's designed to use the following WS2812B light ring:

![image](https://github.com/user-attachments/assets/e80dc6ed-b468-4977-83d6-e0aab0d613a1)

It supports two buttons. One for switching the effect, another for turning the display on/off. See main.py for details, if you need to switch the pins:

```
# button to switch effects
button_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
# button to toggle lights on/off
button_toggle_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
```

## Dependencies

neopixel.py from https://github.com/blaz-r/pi_pico_neopixel.  This need to be copied onto the Pi Pico, along with main.py, and machine.py.

If using the simulator on PC, you'll need to install pygame (https://www.pygame.org/).

```pip install pygame```

### Simulator Instructions

In order to run the simulator, you need pygame installed. 

You can run it with python on a PC with the included mock neopixel.py and utime.py mock libraries (all present in the same directory).  

Installing pygame:

```
pip3 install pygame
```

You can download the code here:
https://github.com/int3grate/doomsday_machine/archive/refs/heads/main.zip

Unzip that file and switch into the directory you unzipped it to using "cd" on terminal.  Then run main.py:

```
python3 main.py
```

<img width="608" alt="image" src="https://github.com/user-attachments/assets/19ba2ddf-01c2-4acc-b7bf-2141ed12184f" />



