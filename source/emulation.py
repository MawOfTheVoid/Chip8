from screen import Screen
from chip8_emulator import Chip8
import pygame


def start_emulation(rom_path, on_pixel_color, off_pixel_color):
    pygame.init()
    off_pixel_color = off_pixel_color[0:3]
    on_pixel_color = on_pixel_color[0:3]
    screen = Screen(on_pixel_color, off_pixel_color)
    chip8 = Chip8(rom_path, screen)
    emu_loop(chip8, screen)

def emu_loop(chip8, screen):
    while True:
        chip8.get_input()
        chip8.fetch_opcode()
        chip8.execute_opcode()
        chip8.count_down_timers()
        screen.draw_matrix()
