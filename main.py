from neopixel import Neopixel
import utime
import random
import math
import machine

current_effect_index = 0
last_button_state = 1
last_debounce_time = 0
debounce_delay = 200  # ms

button_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
button_toggle_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

lights_enabled = True
last_toggle_state = 1
last_toggle_time = 0
toggle_debounce_delay = 200  # ms

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
        'lights_idx': [1, 2, 3, 4, 5, 6, 7, 8],
        'cur_color': None,
        'cur_brightness': None,
        'color_choices': [yellow]
    },
    {
        'id': 2,
        'brightness': 50.0,
        'lights_idx': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        'cur_color': None,
        'cur_brightness': None,
        'color_choices': [red, r1]
    },
    {
        'id': 3,
        'brightness': 50.0,
        'lights_idx': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
        'cur_color': None,
        'cur_brightness': None,
        'color_choices': [o1, m1]
    },
    {
        'id': 4,
        'brightness': 50.0,
        'lights_idx': [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
        'cur_color': None,
        'cur_brightness': None,
        'color_choices': [red, m1]
    },
    {
        'id': 5,
        'brightness': 60.0,
        'lights_idx': [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
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

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB color space (h in range 0–1)"""
    i = int(h * 6)
    f = h * 6 - i
    p = int(255 * v * (1 - s))
    q = int(255 * v * (1 - f * s))
    t = int(255 * v * (1 - (1 - f) * s))
    v = int(255 * v)
    i = i % 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

neural_colors = [
    (90, 0, 120),    # dark purple
    (150, 0, 255),   # magenta
    (0, 50, 150),    # electric blue
    (255, 80, 255),  # neural flash pink
    (50, 0, 100),    # deep cortex glow
    (200, 0, 150),   # glitch pulse
    (20, 0, 40),     # background idle color
]

glitch_pixels = set()
glitch_timer = 0

def random_lightning_color():
    # Pale white-ish yellow or blue tints
    return random.choice([
        (255, 255, 255),    # white
        (255, 250, 200),    # soft flash
        (200, 225, 255)     # lightning blue
    ])

core_state = {
    'phase': 0.0,
    'meltdown_timer': 0,
    'flash_triggered': False
}

def set_strip_color(strip_idx, color, brightness):
    strip_id = 0
    for i in range(0, len(light_rings)):
        if (light_rings[i]['id'] == strip_idx):
            strip_id = i
            break

    strip.brightness(brightness)
    light_rings[strip_id]['cur_brightness'] = brightness

    for i in light_rings[strip_id]['lights_idx']:
        strip.set_pixel(i, color)
        light_rings[strip_id]['cur_color'] = color

    strip.show()

set_strip_color(0, purple, 100)
set_strip_color(1, red, 100)
set_strip_color(2, orange, 100)
set_strip_color(3, red, 100)
set_strip_color(4, red, 100)
set_strip_color(5, m1, 100)

brightness_levels = [25, 50, 75, 100]
update_intervals = [500, 600, 700, 800]

start_time = utime.ticks_ms()

# Constants
reverse_pulse = True

pulse_speed = .5  # lower = slower
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

effect_list = ["STORM_FLASH", "PULSATING", "RAINBOW_SPIRAL", "STORM_FLASH", "CORE_MELTDOWN", "COLOR_NOISE", "HEARTBEAT_CORE"]

effect = effect_list[current_effect_index]

try:
    while True:
        # Button reading and debounce
        button_state = button_pin.value()
        now = utime.ticks_ms()

        if button_state == 0 and last_button_state == 1:
            if utime.ticks_diff(now, last_debounce_time) > debounce_delay:
                # Button was pressed
                current_effect_index = (current_effect_index + 1) % len(effect_list)
                effect = effect_list[current_effect_index]
                print("Switched to effect:", effect)
                last_debounce_time = now

        last_button_state = button_state

        # Toggle on/off button (Pin 2)
        toggle_state = button_toggle_pin.value()

        if toggle_state == 0 and last_toggle_state == 1:
            if utime.ticks_diff(now, last_toggle_time) > toggle_debounce_delay:
                lights_enabled = not lights_enabled
                print("Lights", "enabled" if lights_enabled else "disabled")
                last_toggle_time = now

        last_toggle_state = toggle_state

        if not lights_enabled:
            for i in range(numpix):
                strip.set_pixel(i, (0, 0, 0))
            strip.brightness(0)
            strip.show()
            continue

        t_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
        t = t_ms / 1000.0  # convert to seconds

        if effect == "PULSATING":
            for ring in light_rings:
                phase = ring['pulse_phase']
                brightness = (math.sin(t / pulse_speed + phase) + 1) / 2  # normalize 0–1
                brightness_scaled = int(brightness * 100)  # scale to 0–100

                base_color = base_colors[ring['id']]
                set_strip_color(ring['id'], base_color, brightness_scaled)

        elif effect == "RAINBOW_SPIRAL":
            spiral_speed = 0.2  # controls how fast the spiral spins
            ring_speed = 0.1  # controls how fast it moves outward
            for ring in light_rings:
                ring_phase = ring['pulse_phase']
                num_leds = len(ring['lights_idx'])

                for i, pixel_index in enumerate(ring['lights_idx']):
                    angle_offset = i / num_leds if num_leds > 1 else 0
                    hue = (t * spiral_speed + angle_offset + ring_phase * ring_speed) % 1.0
                    color = hsv_to_rgb(hue, 1, 1)
                    strip.set_pixel(pixel_index, color)

            strip.brightness(100)
            strip.show()

        elif effect == "STORM_FLASH":
            for ring in light_rings:
                phase = ring['pulse_phase']
                base = base_colors[ring['id']]
                brightness = (math.sin(t / pulse_speed + phase) + 1) / 2  # normalize
                brightness_scaled = int(brightness * 70 + 30)  # don't go fully dark

                set_strip_color(ring['id'], base, brightness_scaled)

            # Occasionally trigger lightning
            if random.random() < 0.10:  # ~10% chance per frame
                lightning_ring = random.choice(light_rings)
                for i in lightning_ring['lights_idx']:
                    color = random_lightning_color()
                    strip.set_pixel(i, color)
                strip.brightness(100)
                strip.show()
                utime.sleep_ms(50)  # flash duration

                # Reset to base color
                for i in lightning_ring['lights_idx']:
                    strip.set_pixel(i, lightning_ring['cur_color'] or off)
                strip.brightness(lightning_ring['cur_brightness'] or 50)
                strip.show()

        elif effect == "CORE_MELTDOWN":
            # Gradual intensity increase
            core_state['phase'] += 0.03
            meltdown_timer = core_state['meltdown_timer']
            flash_triggered = core_state['flash_triggered']

            # Sine wave brightness, speeding up over time
            speed = 0.5 - min(0.4, core_state['phase'] * 0.02)  # goes from 0.5 to 0.1
            brightness = (math.sin(t / speed) + 1) / 2
            brightness_scaled = int(brightness * 100)

            # Color progression: orange → red → white
            progress = min(core_state['phase'], 1.0)
            r = int(240 + progress * (255 - 240))
            g = int(50 - progress * 50)
            b = int(progress * 255)
            base_color = (r, g, b)

            # Set all rings to that color
            for ring in light_rings:
                set_strip_color(ring['id'], base_color, brightness_scaled)

            # Once meltdown phase is long enough, trigger flash
            if core_state['phase'] >= 1.0 and not flash_triggered:
                # FLASH! Full white
                for ring in light_rings:
                    set_strip_color(ring['id'], (255, 255, 255), 100)
                utime.sleep_ms(100)
                core_state['flash_triggered'] = True
                core_state['meltdown_timer'] = 10  # cooldown countdown frames

            # After flash, fade back to ominous glow
            if flash_triggered:
                core_state['meltdown_timer'] -= 1
                if core_state['meltdown_timer'] <= 0:
                    # Reset phase
                    core_state['phase'] = 0
                    core_state['flash_triggered'] = False

        elif effect == "COLOR_NOISE":
            for i in range(numpix):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                strip.set_pixel(i, (r, g, b))
            strip.brightness(100)
            strip.show()

        elif effect == "HEARTBEAT_CORE":
            # Beat: sine wave controlling brightness (0 to 1)
            beat_speed = 2.0
            beat_phase = (math.sin(t * (math.pi * 2 / beat_speed)) + 1) / 2
            pulse_brightness = int((beat_phase ** 4) * 100)  # quick spike, slow fade

            # White pulse in center
            core_color = (255, 255, 255) if pulse_brightness > 20 else (50, 0, 0)
            set_strip_color(0, core_color, pulse_brightness)
            set_strip_color(1, core_color, pulse_brightness)

            # Outer ring flicker (subtle random brightness)
            for ring_id in range(2, 6):
                flicker = random.randint(-10, 10)  # add chaos
                base_brightness = 60
                flicker_brightness = max(30, min(100, base_brightness + flicker))
                set_strip_color(ring_id, (120, 0, 0), flicker_brightness)

        utime.sleep_ms(30)

except SystemExit:
    print("Simulator closed.")
