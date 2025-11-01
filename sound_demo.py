import pygame
import pygame._sdl2.audio as sdl2_audio
import time


def get_devices(capture_devices: bool = False) -> tuple[str, ...]:
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    return devices


def play(file_path: str, device: str | None = None):
    if device is None:
        devices = get_devices()
        if not devices:
            raise RuntimeError("No device!")
        device = devices[0]
    print("Play: {}\r\nDevice: {}".format(file_path, device))
    pygame.mixer.init(devicename=device, buffer=4096)
    print("PyGame init params: " + str(pygame.mixer.get_init()))
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    crash_sfx = pygame.mixer.Sound("assets/crash.mp3")
    try:
        while True:
            crash_sfx.play()
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    pygame.mixer.quit()


if __name__ == "__main__":
    play("assets/example.mp3")
    devices = get_devices()
