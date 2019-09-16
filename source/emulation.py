from screen import Screen
from chip8_emulator import Chip8


def start_emulation(rom_path, on_pixel_color, off_pixel_color):
    off_pixel_color = off_pixel_color[0:3]
    on_pixel_color = on_pixel_color[0:3]
    screen = Screen(on_pixel_color, off_pixel_color)
    chip8 = Chip8(rom_path, screen)
    emu_loop(chip8, screen)

def emu_loop(chip8, screen):
    print("moin")
