from neopixel import Neopixel
import utime 
import random
import math

numpix = 81

# Define the colors you want to use
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (240, 50, 0)
purple = (100, 0, 250)
off = (0, 0, 0)

# custom colors
p1 = (107, 52, 235)
r1 = (242, 50, 0)

o1 = (245, 100, 0)
m1 = (245, 5, 0)

light_rings = [
{
    'id': 0,
    'brightness': 50.0,
    'lights_idx': [0],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [orange, yellow]
},
{
    'id': 1,
    'brightness': 50.0,
    'lights_idx': [1,2,3,4,5,6,7,8],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [yellow]
},
{
    'id': 2,
    'brightness': 50.0,
    'lights_idx': [9,10,11,12,13,14,15,16,17,18,19,20],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [red, r1]
},
{
    'id': 3,
    'brightness': 50.0,
    'lights_idx': [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [o1, m1]
},
{
    'id': 4,
    'brightness': 50.0,
    'lights_idx': [37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [red, m1]
},
{
    'id': 5,
    'brightness': 60.0,
    'lights_idx': [57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80],
    'cur_color': None,
    'cur_brightness': None,
    'color_choices': [red]
}
]

is_simulator = None

try:
    import neopixel
    if hasattr(neopixel, "__version__") and neopixel.__version__ == "simulator":
        is_simulator = True
    else:
        is_simulator = False
except ImportError:
    is_simulator = False

if is_simulator:
    strip = Neopixel(numpix, 0, 0, "GRB", light_rings)
else:
    strip = Neopixel(numpix, 0, 0, "GRB")

def set_strip_color(strip_idx, color, brightness):
    strip_id = 0
    for i in range(0, len(light_rings)):
        if(light_rings[i]['id'] == strip_idx):
            strip_id = i
            break

    strip.brightness(brightness)
    light_rings[strip_id]['cur_brightness'] = brightness
    
    for i in light_rings[strip_id]['lights_idx']:
        strip.set_pixel(i, color)
        light_rings[strip_id]['cur_color'] = color
        
    strip.show()
  
set_strip_color(0,purple,100)
set_strip_color(1,red,100)
set_strip_color(2,orange,100)
set_strip_color(3,red,100)
set_strip_color(4,red,100)
set_strip_color(5,m1,100)

brightness_levels = [25, 50, 75, 100]
update_intervals = [500, 600, 700, 800]

start_time = utime.ticks_ms()

# Constants
reverse_pulse = True

pulse_speed = .5 # lower = slower
base_colors = {
    0: yellow,
    1: yellow,
    2: orange,
    3: r1,
    4: red,
    5: red
}

# adjust phase spacing for ripple (can be greater than one)
phase_spacing = .6

# Assign phase offset to each ring based on distance from center
for i, ring in enumerate(light_rings):
    ring_index = len(light_rings) - 1 - i if reverse_pulse else i
    ring['pulse_phase'] = ring_index * phase_spacing

try:
    while True:
        t_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
        t = t_ms / 1000.0  # convert to seconds

        for ring in light_rings:
            phase = ring['pulse_phase']
            brightness = (math.sin(t / pulse_speed + phase) + 1) / 2  # normalize 0–1
            brightness_scaled = int(brightness * 100)  # scale to 0–100

            base_color = base_colors[ring['id']]
            set_strip_color(ring['id'], base_color, brightness_scaled)

        utime.sleep_ms(30)

except SystemExit:
    print("Simulator closed.")
