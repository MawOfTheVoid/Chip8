import binascii
import pygame
import sys

class Chip8():

    def __init__(self, rom_path, screen):
        self.rom_path = rom_path
        self.screen = screen
        self.memory = self.prepare_memory()
        self.pc = 512
        self.I_register = 0
        self.stack = []
        self.delay_timer = 0
        self.music_timer = 0
        self.keyboard_register = []
        self.opcode = 0

    def get_input(self):
        for event in pygame.event.get():
            self.system_relevant_keypress(event)
            self.game_keydown(event)
            self.game_keyup(event)

    def system_relevant_keypress(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            self.screen.resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.screen.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                sys.exit()

    def game_keydown(self, event):
        pass

    def game_keyup(self, event):
        pass

    def fetch_opcode(self):
        part_one = self.memory[self.pc]
        part_two = self.memory[self.pc+1]
        part_one = part_one << 8
        self.opcode = part_one + part_two
        #self.pc += 2

    def execute_opcode(self):
        pass

    def count_down_timers(self):
        pass

    def prepare_memory(self):
        memory = self.memory_fonts()
        memory += 432 * [0]
        memory += self.load_rom(memory)
        memory += (4096 - len(memory)) * [0]
        return memory

    def load_rom(self, memory):
        with open(self.rom_path, "rb") as file_obj:
            rom = file_obj.read()
        rom = binascii.hexlify(rom)
        # split rom into two hex values each
        rom = [rom[i:i + 2] for i in range(0, len(rom), 2)]
        # converts them from binary string to normal string
        rom = [int(register, 16) for register in rom]
        return rom


    def memory_fonts(self):
        fonts = [
            240, 144, 144, 144, 240,
            32, 96, 32, 32, 112,
            240, 16, 240, 128, 240,
            240, 16, 240, 16, 240,
            144, 144, 240, 16, 16,
            240, 128, 240, 16, 240,
            240, 128, 240, 144, 240,
            240, 16, 32, 64, 64,
            240, 144, 240, 144, 240,
            240, 144, 240, 16, 240,
            240, 144, 240, 144, 144,
            224, 144, 224, 144, 224,
            240, 128, 128, 128, 240,
            224, 144, 144, 144, 224,
            240, 128, 240, 128, 240,
            240, 128, 240, 128, 128
        ]
        return fonts