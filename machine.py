import random

class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 2
    PULL_DOWN = 3

    def __init__(self, pin_num, mode=IN, pull=None):
        self.pin_num = pin_num
        self.mode = mode
        self.pull = pull
        self._value = 1  # default HIGH (not pressed for pull-up)
        self._simulate_pressed = False
        self._press_counter = 0

    def value(self):
        # Simulate button press every 300 frames or so
        self._press_counter += 1
        if self._press_counter > 300:
            self._simulate_pressed = not self._simulate_pressed
            self._press_counter = 0

        return 0 if self._simulate_pressed else 1

    def simulate_press(self):
        self._simulate_pressed = True

    def simulate_release(self):
        self._simulate_pressed = False
