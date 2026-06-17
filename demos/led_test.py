#!/usr/bin/env python3
"""
WS2812b LED test script — Raspberry Pi 4, GPIO 21
Requires: sudo pip install rpi_ws281x adafruit-circuitpython-neopixel --break-system-packages
Run with: sudo python3 ws2812b_test.py
"""

import time
import board
import neopixel

# ── Config ────────────────────────────────────────────────────────────────────
PIN        = board.D21   # GPIO 21
NUM_LEDS   = 44          # adjust to your strip length
BRIGHTNESS = 0.4         # 0.0–1.0  (keep low for bench testing)
ORDER      = neopixel.GRB  # most WS2812b strips are GRB
# ─────────────────────────────────────────────────────────────────────────────

pixels = neopixel.NeoPixel(
    PIN, NUM_LEDS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=ORDER,
)


def fill(color, delay=0.5):
    pixels.fill(color)
    pixels.show()
    time.sleep(delay)


def wipe(color, delay=0.03):
    """Light each pixel one at a time."""
    for i in range(NUM_LEDS):
        pixels[i] = color
        pixels.show()
        time.sleep(delay)


def chase(color, delay=0.05, passes=3):
    """Single-pixel theatre-chase."""
    for _ in range(passes):
        for i in range(NUM_LEDS):
            pixels.fill((0, 0, 0))
            pixels[i] = color
            pixels.show()
            time.sleep(delay)


def rainbow_cycle(delay=0.01, passes=2):
    """Full rainbow across the strip."""
    def wheel(pos):
        pos = pos % 255
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    for _ in range(passes):
        for j in range(256):
            for i in range(NUM_LEDS):
                pixels[i] = wheel((i * 256 // NUM_LEDS + j) & 255)
            pixels.show()
            time.sleep(delay)


def blink(color, times=5, delay=0.3):
    for _ in range(times):
        fill(color, delay)
        fill((0, 0, 0), delay)


if __name__ == "__main__":
    print(f"Testing {NUM_LEDS} LEDs on GPIO 21 — Ctrl+C to stop\n")
    try:
        print("1. Solid red/green/blue")
        for c in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
            fill(c, 1.0)

        print("2. White fill")
        fill((255, 255, 255), 100.0)

        print("3. Color wipe")
        for c in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
            wipe(c)

        print("4. Theatre chase")
        chase((255, 165, 0))

        print("5. Rainbow cycle")
        rainbow_cycle()

        print("6. Blink")
        blink((0, 200, 255))

        print("Done.")

    except KeyboardInterrupt:
        pass
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("LEDs off.")