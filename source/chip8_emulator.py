from opcode_variables import get_nnn, get_x, get_y, get_kk, get_n
from PySide2 import QtWidgets
from random import randint
import binascii
import pygame
import sys


class Chip8():

    def __init__(self, rom_path, screen):
        self.assign_dicts()
        self.rom_path = rom_path
        self.screen = screen
        self.memory = self.prepare_memory()
        self.pc = 512
        self.register = 16 * [0]
        self.I_register = 0
        self.stack = []
        self.delay_timer = 0
        self.music_timer = 0
        self.keyboard_register = 16 * [0]
        self.opcode = 0
        self.sound = pygame.mixer.Sound("chip8_sound.wav")
        self.sound.play(loops=-1)
        pygame.mixer.pause()

    def assign_dicts(self):
        self.function_switch = {
            0x0: self.zero_functions,
            0x1: self.op_1nnn,
            0x2: self.op_2nnn,
            0x3: self.op_3xkk,
            0x4: self.op_4xkk,
            0x5: self.op_5xy0,
            0x6: self.op_6xkk,
            0x7: self.op_7xkk,
            0x8: self.eight_functions,
            0x9: self.op_9xy0,
            0xA: self.op_Annn,
            0xB: self.op_Bnnn,
            0xC: self.op_Cxkk,
            0xD: self.op_Dxyn,
            0xE: self.e_functions,
            0xF: self.f_functions,
        }

        self.zero_opcodes = {
            0xE0: self.op_00E0,
            0xEE: self.op_00EE,
            0x00: lambda: None
        }

        self.eight_opcodes = {
            0x0: self.op_8xy0,
            0x1: self.op_8xy1,
            0x2: self.op_8xy2,
            0x3: self.op_8xy3,
            0x4: self.op_8xy4,
            0x5: self.op_8xy5,
            0x6: self.op_8xy6,
            0x7: self.op_8xy7,
            0xE: self.op_8xyE
        }

        self.e_opcodes = {
            0x9E: self.op_Ex9E,
            0xA1: self.op_ExA1
        }

        self.f_opcodes = {
            0x07: self.op_Fx07,
            0x0A: self.op_Fx0A,
            0x15: self.op_Fx15,
            0x18: self.op_Fx18,
            0x1E: self.op_Fx1E,
            0x29: self.op_Fx29,
            0x33: self.op_Fx33,
            0x55: self.op_Fx55,
            0x65: self.op_Fx65
        }

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
        self.opcode = part_one | part_two
        self.pc += 2

    def execute_opcode(self):
        opcode_identifier = self.opcode >> 12
        self.function_switch[opcode_identifier]()


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

    def zero_functions(self):
        opcode_identifier = self.opcode & 0xFF
        try:
            self.zero_opcodes[opcode_identifier]()
        except Exception:
            QtWidgets.QMessageBox.warning(
                None, 'Error',
                'Unsupported Opcode "0nnn"',
                QtWidgets.QMessageBox.Ok)

    def eight_functions(self):
        opcode_identifier = self.opcode & 0xF
        self.eight_opcodes[opcode_identifier]()

    def e_functions(self):
        opcode_identifier = self.opcode & 0xFF
        self.e_opcodes[opcode_identifier]()

    def f_functions(self):
        opcode_identifier = self.opcode & 0xFF
        self.f_opcodes[opcode_identifier]()

    def op_00E0(self):
        #print("00E0")
        for row in self.screen.screen_matrix:
            for index, pixel in enumerate(row):
                row[index] = 0

    def op_00EE(self):
        #print("00EE")
        self.pc = self.stack.pop()

    def op_1nnn(self):
        ##print("1nnn")
        nnn = get_nnn(self.opcode)
        #print("1nnn", hex(nnn))
        self.pc = nnn

    def op_2nnn(self):
        #print("2nnn")
        nnn = get_nnn(self.opcode)
        adress = self.pc
        self.stack.append(adress)
        self.pc = nnn
        #print("2nnn", f"nnn={hex(nnn)}  ", f"self.pc={hex(self.pc)} ", f"adress={hex(adress)}   ", f"memory_value_after_jump={hex(self.memory[self.pc])}")

    def op_3xkk(self):
        x = get_x(self.opcode)
        kk = get_kk(self.opcode)
        #print("3xkk", f"x={hex(x)}", f"kk={hex(kk)}")
        if self.register[x] == kk:
            self.pc += 2

    def op_4xkk(self):
        #print("4xkk")
        x = get_x(self.opcode)
        kk = get_kk(self.opcode)
        if self.register[x] != kk:
            self.pc += 2

    def op_5xy0(self):
        #print("5xy0")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        if self.register[x] == self.register[y]:
            self.pc += 2

    def op_6xkk(self):
        x = get_x(self.opcode)
        kk = get_kk(self.opcode)
        #print("6xkk", f"x={hex(x)}", f"kk={hex(kk)}")
        self.register[x] = kk

    def op_7xkk(self):
        #print("7xkk")
        x = get_x(self.opcode)
        kk = get_kk(self.opcode)
        self.register[x] = kk + self.register[x]
        if self.register[x] > 255:
            self.register[x] = self.register[x] & 0xFF

    def op_8xy0(self):
        #print("8xy0")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] = self.register[y]

    def op_8xy1(self):
        #print("8xy1")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] = self.register[x] | self.register[y]

    def op_8xy2(self):
        #print("8xy2")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] = self.register[x] & self.register[y]

    def op_8xy3(self):
        #print("8xy3")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] = self.register[x] ^ self.register[y]

    def op_8xy4(self):
        #print("8xy4")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] += self.register[y]
        if self.register[x] > 255:
            self.register[x] = self.register[x] & 0xFF
            self.register[15] = 1
        elif self.register[x] <= 255:
            self.register[15] = 0

    def op_8xy5(self):
        #print("8xy5")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] -= self.register[y]
        if self.register[x] <= 0:
            self.register[15] = 0
            self.register[x] = self.register[x] & 0xFF
        elif self.register[x] > 0:
            self.register[15] = 1

    def op_8xy6(self):
        #print("8xy6")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[15] = self.register[x] & 0x0001
        self.register[x] = self.register[x] // 2

    def op_8xy7(self):
        #print("8xy7")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[x] = self.register[y] - self.register[x]
        if self.register[x] < 0:
            self.register[15] = 0
            self.register[x] = self.register[x] & 0xFF
        elif self.register[x] >= 0:
            self.register[15] = 1

    def op_8xyE(self):
        #print("8xyE")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        self.register[15] = self.register[x] & 0x80
        self.register[x] *= 2
        if self.register[x] > 255:
            self.register[x] = self.register[x] & 0xFF

    def op_9xy0(self):
        #print("9xy0")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        if self.register[x] != self.register[y]:
            self.pc += 2

    def op_Annn(self):
        #print("Annn")
        nnn = get_nnn(self.opcode)
        self.I_register = nnn

    def op_Bnnn(self):
        #print("Bnnn")
        nnn = get_nnn(self.opcode)
        self.pc = nnn + self.register[0]

    def op_Cxkk(self):
        #print("Cxkk")
        x = get_x(self.opcode)
        kk = get_kk(self.opcode)
        rand = randint(0, 255)
        self.register[x] = kk & rand

    def op_Dxyn(self):
        #print("Dxyn")
        x = get_x(self.opcode)
        y = get_y(self.opcode)
        n = get_n(self.opcode)
        drawable_chunk = self.get_binary_array(n)
        for y_index, row in enumerate(drawable_chunk):
            for x_index, pixel_bit in enumerate(row):
                current_y, current_x = self.get_coordinates(y, y_index, x, x_index)
                self.draw_pixel_to_array(pixel_bit, current_y, current_x)


    def op_Ex9E(self):
        #print("Ex9E")
        x = get_x(self.opcode)
        if self.keyboard_register[self.register[x]]:
            self.pc += 2

    def op_ExA1(self):
        #print("ExA1")
        x = get_x(self.opcode)
        if not self.keyboard_register[self.register[x]]:
            self.pc += 2

    def op_Fx07(self):
        #print("Fx07")
        x = get_x(self.opcode)
        self.register[x] = self.delay_timer

    def op_Fx0A(self):
        #print("Fx0A")
        x = get_x(self.opcode)
        not_pressed = True
        while not_pressed:
            for event in pygame.event.get():
                self.system_relevant_keypress(event)
                self.game_keydown(event)
                self.game_keyup(event)
                for index, key in enumerate(self.keyboard_register):
                    if key:
                        self.register[x] = index
                        not_pressed = False


    def op_Fx15(self):
        #print("Fx15")
        x = get_x(self.opcode)
        self.delay_timer = self.register[x]

    def op_Fx18(self):
        #print("Fx18")
        x = get_x(self.opcode)
        self.music_timer = self.register[x]

    def op_Fx1E(self):
        #print("Fx1E")
        x = get_x(self.opcode)
        self.I_register += x

    def op_Fx29(self):
        #print("Fx29")
        x = get_x(self.opcode)
        self.I_register = self.register[x] * 5


    def op_Fx33(self):
        #print("Fx33")
        x = get_x(self.opcode)
        bcd_repr = self.get_binary_decimal(x)
        for index, number in enumerate(bcd_repr):
            self.memory[self.I_register + index] = number

    def op_Fx55(self):
        #print("Fx55")
        x = get_x(self.opcode)
        for index, value in enumerate(self.register):
            self.memory[self.I_register + index] = value
            if index == x:
                break

    def op_Fx65(self):
        #print("Fx65")
        x = get_x(self.opcode)
        for index, value in enumerate(self.register):
            self.register[index] = self.memory[self.I_register + index]
            if index == x:
                break

    def get_binary_array(self, n):
        drawable_chunk = self.memory[self.I_register:self.I_register+n]
        for index, byte in enumerate(drawable_chunk):
            drawable_chunk[index] = self.byte_to_array(byte)
        return drawable_chunk

    def byte_to_array(self, byte):
        array = []
        for a in range(0, 8):
            last = byte & 0x01
            byte = byte >> 1
            array.insert(0, last)
        return array

    def get_coordinates(self, y, y_index, x, x_index):
        current_y = self.register[y] + y_index
        current_x = self.register[x] + x_index
        # - screen_width / height to account for 0
        if current_y > 31:
            current_y -= 32
        if current_x > 63:
            current_x -= 64
        return current_y, current_x

    def draw_pixel_to_array(self, pixel_value, current_y, current_x):
        screen_value = self.screen.screen_matrix[current_y][current_x]
        if screen_value and pixel_value:
            self.register[15] = 1
        self.screen.screen_matrix[current_y][current_x] = screen_value ^ pixel_value

    def get_binary_decimal(self, x):
        x = list(str(x))
        x = [int(digit) for digit in x]
        if len(x) == 3:
            hundreds, tens, ones = x
        elif len(x) == 2:
            tens, ones = x
            hundreds = 0
        elif len(x) == 1:
            ones = x[0]
            hundreds, tens = 0, 0
        return [hundreds, tens, ones]
