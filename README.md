# Lego Duck Race

Code and setup instructions for the Lego Duck Race project presented at Brickworld 2025.

## Hardware

* Raspberry Pi 4
* Raspberry Pi Build HAT + Power Supply
* [Large Lego Technic Motor](https://www.lego.com/en-us/product/technic-large-motor-88013) x3
* Arcade style buttons from [Micro Center Arcade Kit](https://www.microcenter.com/product/645997/universal-arcade-control-kit-black)
* Limit switches on GPIO pins 27, 5, and 26

## Software

* Raspberry Pi OS Lite (Debian Bookworm)
* Python dependencies are managed with `uv` and `pyproject.toml`
* Hardware dependencies are optional so tests and core code can run on non-Pi machines

```bash
uv sync                # development/core dependencies
uv sync --extra hardware  # Raspberry Pi hardware dependencies
```

## Project structure

* `lego_duck_race.core` contains hardware-independent game and lane logic.
* `lego_duck_race.interfaces` contains shared controller and motor interfaces.
* `lego_duck_race.hardware` contains Build HAT, GPIO, and HID implementations.

## Running diagnostics

Run these on the Raspberry Pi before starting the full game:

```bash
uv run controller_test  # HID arcade controller metadata, joystick, and button state
uv run motor_test       # Build HAT motor connection and forward/backward/stop checks
uv run switch_test      # GPIO limit switch press checks
uv run hardware_test    # Interactive combined diagnostics
```

## Running the code

```bash
uv run game   # Run the main Lego Duck Race game using real hardware
uv run demo   # Run a simplified hardware demo
uv run ascii  # Run an ASCII simulation of the game
```

## Lane mapping

Lane configuration lives in `src/lego_duck_race/config/lanes.yaml`:

```yaml
lanes:
  - name: A
    button_name: k1
    limit_switch_gpio: 27
```

The lane `name` is also used as the Build HAT motor port and limit-switch mapping key, so those values always match. `limit_switch_gpio` configures the GPIO pin for that lane's switch. To use a different config file at runtime, set:

```bash
export LEGO_DUCK_RACE_LANE_CONFIG=/path/to/lanes.yaml
```

Current default mapping:

| Lane / Motor Port / Switch Name | Controller Button | Limit Switch GPIO |
|---------------------------------|-------------------|-------------------|
| A                               | k1                | 27                |
| B                               | k2                | 5                 |
| C                               | k3                | 26                |
