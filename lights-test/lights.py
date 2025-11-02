import time

import board
import neopixel
from rainbowio import colorwheel

red = (100, 0, 0)
green = (0, 100, 0)
blue = (0, 0, 100)
white = (100, 100, 100)

test_pattern = (red, green, blue, white)


def rainbow_cycle(wait, pixels):
    for color in range(255):
        for pixel in range(len(pixels)):  # pylint: disable=consider-using-enumerate
            pixel_index = (pixel * 256 // len(pixels)) + color * 5
            pixels[pixel] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def rgb_test(pixels):
    for i in range(0, len(pixels)):
        pixels[i] = test_pattern[i % len(test_pattern)]
    pixels.show()
    time.sleep(2)


def clear(pixels):
    for i in range(0, len(test_pattern)):
        pixels[i] = 0


strip = neopixel.NeoPixel(board.D10, 8, auto_write=False)

print("RGB Test Pattern")
rgb_test(strip)

print("Rainbow Test Pattern")
rainbow_cycle(0.05, strip)

print("RGB Test Pattern")
rgb_test(strip)
