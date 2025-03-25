import pygame
import math
import sys
import threading

__version__ = "simulator"
debug = True

def start_simulator_in_thread(simulator):
    def run():
        clock = pygame.time.Clock()
        while simulator.running:
            simulator.handle_events()
            clock.tick(30)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread

class Strip:
    def __init__(self, num_pixels, light_rings):
        self.num_pixels = num_pixels
        self.cur_brightness = 0
        # black default
        self.pixels = [(0,0,0)] * num_pixels
        self.brightnesses = [0] * num_pixels
        self.light_rings = light_rings
        self.simulator = DisplaySimulator(self.num_pixels, self.light_rings)
        start_simulator_in_thread(self.simulator)

    def set_pixel(self, id, color):
        self.pixels[id] = color
        self.brightnesses[id] = self.cur_brightness
        if debug:
            print(f'Setting pixel {id} to {color}')

    def brightness(self, brightness):
        self.cur_brightness = brightness
        if debug:
            print(f'Setting brightness to {self.cur_brightness}')

    def show(self):
        if debug:
            print(f'Showing strip')
        self.simulator.render(self.pixels, self.brightnesses)

def Neopixel(num_pix, a, b, color_mode, lr):
    if debug:
        print("Called Neopixel()")
    return Strip(num_pix, light_rings=lr)

class DisplaySimulator:
    def __init__(self, num_pixels, light_rings=None):
        pygame.init()
        self.num_pixels = num_pixels
        self.light_rings = light_rings
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pixel Display Simulation")
        self.center = (400, 400)
        self.base_radius = 30
        self.radius_step = 40
        self.running = True

        # Build pixel layout using light_rings
        self.pixel_positions = [None] * num_pixels
        if light_rings is not None:
            self._layout_from_rings()

    def _layout_from_rings(self):
        for ring in self.light_rings:
            ring_id = ring['id']
            idxs = ring['lights_idx']
            radius = self.base_radius + self.radius_step * ring_id
            count = len(idxs)
            for i, pixel_id in enumerate(idxs):
                if count == 1:  # Center pixel
                    x, y = self.center
                else:
                    angle_deg = (360 / count) * i
                    angle_rad = math.radians(angle_deg)
                    x = int(self.center[0] + radius * math.cos(angle_rad))
                    y = int(self.center[1] + radius * math.sin(angle_rad))
                self.pixel_positions[pixel_id] = (x, y)

    def adjust_brightness(self, color, brightness_percent):
        return tuple(min(255, max(0, int(c * (brightness_percent / 100.0)))) for c in color)

    def render(self, pixel_colors, brightnesses):
        self.handle_events()
        self.screen.fill((0, 0, 0))

        for idx, color in enumerate(pixel_colors):
            if self.pixel_positions[idx] is None:
                continue  # Pixel not placed
            brightness = brightnesses[idx]
            adjusted_color = self.adjust_brightness(color, brightness)
            pygame.draw.circle(self.screen, adjusted_color, self.pixel_positions[idx], 10)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
