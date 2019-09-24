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
        self.keyboard_register = 16 * [0]
        self.opcode = 0
        self.sound = pygame.mixer.Sound("chip8_sound.wav")
        self.sound.play(loops=-1)
        pygame.mixer.pause()

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.keyboard_register[0] = 1
            elif event.key == pygame.K_1:
                self.keyboard_register[1] = 1
            elif event.key == pygame.K_2:
                self.keyboard_register[2] = 1
            elif event.key == pygame.K_3:
                self.keyboard_register[3] = 1
            elif event.key == pygame.K_q:
                self.keyboard_register[4] = 1
            elif event.key == pygame.K_w:
                self.keyboard_register[5] = 1
            elif event.key == pygame.K_e:
                self.keyboard_register[6] = 1
            elif event.key == pygame.K_a:
                self.keyboard_register[7] = 1
            elif event.key == pygame.K_s:
                self.keyboard_register[8] = 1
            elif event.key == pygame.K_d:
                self.keyboard_register[9] = 1
            elif event.key == pygame.K_y:
                self.keyboard_register[10] = 1
            elif event.key == pygame.K_c:
                self.keyboard_register[11] = 1
            elif event.key == pygame.K_4:
                self.keyboard_register[12] = 1
            elif event.key == pygame.K_r:
                self.keyboard_register[13] = 1
            elif event.key == pygame.K_f:
                self.keyboard_register[14] = 1
            elif event.key == pygame.K_v:
                self.keyboard_register[15] = 1

    def game_keyup(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                self.keyboard_register[0] = 0
            elif event.key == pygame.K_1:
                self.keyboard_register[1] = 0
            elif event.key == pygame.K_2:
                self.keyboard_register[2] = 0
            elif event.key == pygame.K_3:
                self.keyboard_register[3] = 0
            elif event.key == pygame.K_q:
                self.keyboard_register[4] = 0
            elif event.key == pygame.K_w:
                self.keyboard_register[5] = 0
            elif event.key == pygame.K_e:
                self.keyboard_register[6] = 0
            elif event.key == pygame.K_a:
                self.keyboard_register[7] = 0
            elif event.key == pygame.K_s:
                self.keyboard_register[8] = 0
            elif event.key == pygame.K_d:
                self.keyboard_register[9] = 0
            elif event.key == pygame.K_y:
                self.keyboard_register[10] = 0
            elif event.key == pygame.K_c:
                self.keyboard_register[11] = 0
            elif event.key == pygame.K_4:
                self.keyboard_register[12] = 0
            elif event.key == pygame.K_r:
                self.keyboard_register[13] = 0
            elif event.key == pygame.K_f:
                self.keyboard_register[14] = 0
            elif event.key == pygame.K_v:
                self.keyboard_register[15] = 0

    def fetch_opcode(self):
        part_one = self.memory[self.pc]
        part_two = self.memory[self.pc + 1]
        part_one = part_one << 8
        self.opcode = part_one + part_two
        # self.pc += 2

    def execute_opcode(self):
        try:
            if self.opcode == 0x00E0:
                self.op_00E0(self.opcode)
            elif self.opcode == 0x00EE:
                self.op_00EE(self.opcode)
            elif self.opcode & 0x1000 == 0x1000:
                self.op_1nnn(self.opcode)
            elif self.opcode & 0x2000 == 0x2000:
                self.op_2nnn(self.opcode)
            elif self.opcode & 0x3000 == 0x3000:
                self.op_3xkk(self.opcode)
            elif self.opcode & 0x4000 == 0x4000:
                self.op_4xkk(self.opcode)
            elif self.opcode & 0x5000 == 0x5000:
                self.op_5xy0(self.opcode)
            elif self.opcode & 0x6000 == 0x6000:
                self.op_6xkk(self.opcode)
            elif self.opcode & 0x7000 == 0x7000:
                self.op_7xkk(self.opcode)
            elif self.opcode & 0x8000 == 0x8000:
                self.op_8xy0(self.opcode)
            elif self.opcode & 0x8001 == 0x8001:
                self.op_8xy1(self.opcode)
            elif self.opcode & 0x8001 == 0x8001:
                self.op_8xy1(self.opcode)
            elif self.opcode & 0x8002 == 0x8002:
                self.op_8xy2(self.opcode)
            elif self.opcode & 0x8003 == 0x8003:
                self.op_8xy3(self.opcode)
            elif self.opcode & 0x8004 == 0x8004:
                self.op_8xy4(self.opcode)
            elif self.opcode & 0x8005 == 0x8005:
                self.op_8xy5(self.opcode)
            elif self.opcode & 0x8006 == 0x8006:
                self.op_8xy6(self.opcode)
            elif self.opcode & 0x8007 == 0x8007:
                self.op_8xy7(self.opcode)
            elif self.opcode & 0x800e == 0x800e:
                self.op_8xyE(self.opcode)
            elif self.opcode & 0x9000 == 0x9000:
                self.op_9xy0(self.opcode)
            elif self.opcode & 0xA000 == 0xA000:
                self.op_Annn(self.opcode)
            elif self.opcode & 0xB000 == 0xB000:
                self.op_Bnnn(self.opcode)
            elif self.opcode & 0xC000 == 0xC000:
                self.op_Cxkk(self.opcode)
            elif self.opcode & 0xD000 == 0xD000:
                self.op_Dxyn(self.opcode)
            elif self.opcode & 0xE09E == 0xE09E:
                self.op_Ex9E(self.opcode)
            elif self.opcode & 0xE0A1 == 0xE0A1:
                self.op_ExA1(self.opcode)
            elif self.opcode & 0xF007 == 0xF007:
                self.op_Fx07(self.opcode)
            elif self.opcode & 0xF00A == 0xF00A:
                self.op_Fx0A(self.opcode)
            elif self.opcode & 0xF015 == 0xF015:
                self.op_Fx15(self.opcode)
            elif self.opcode & 0xF018 == 0xF018:
                self.op_Fx18(self.opcode)
            elif self.opcode & 0xF01E == 0xF01E:
                self.op_Fx1E(self.opcode)
            elif self.opcode & 0xF029 == 0xF029:
                self.op_Fx29(self.opcode)
            elif self.opcode & 0xF033 == 0xF033:
                self.op_Fx33(self.opcode)
            elif self.opcode & 0xF055 == 0xF055:
                self.op_Fx55(self.opcode)
            elif self.opcode & 0xF065 == 0xF065:
                self.op_Fx65(self.opcode)
        except Exception as e:
            print(e)


    def count_down_timers(self):
         self.count_down_delay_timer()
         self.count_down_music_timer()

    def count_down_delay_timer(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

    def count_down_music_timer(self):
        if self.music_timer > 0:
            self.music_timer -= 1
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

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
