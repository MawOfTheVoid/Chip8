import binascii

class Chip8():

    def __init__(self, rom_path, screen):
        self.rom_path = rom_path
        self.screen_matrix = screen.screen_matrix
        self.memory = self.prepare_memory()
        self.pc = 512
        self.I_register = 0
        self.stack = []
        self.delay_timer = 0
        self.music_timer = 0
        self.keyboard_register = []
        self.opcode = ""

    def get_input(self):
        pass

    def fetch_opcode(self):
        pass

    def execute_opcode(self):
        pass

    def count_down_timers(self):
        pass

    def prepare_memory(self):
        memory = self.memory_fonts()
        memory += 432 * [0]
        memory += self.load_rom(memory)
        memory += (4096 - len(memory)) * [0]
        self.memory = memory

    def load_rom(self, memory):
        with open(self.rom_path, "rb") as file_obj:
            rom = file_obj.read()
        rom = binascii.hexlify(rom)
        # split rom into two hex values each
        rom = [rom[i:i + 2] for i in range(0, len(rom), 2)]
        # converts them from binary string to normal string
        rom = [hex(int(register, 16)) for register in rom]
        return rom


    def memory_fonts(self):
        fonts = [
            # font for 0
            "0xF0", "0x90", "0x90", "0x90", "0xF0",
            # font for 1
            "0x20", "0x60", "0x20", "0x20", "0x70",
            "0xF0", "0x10", "0xF0", "0x80", "0xF0",
            "0xF0", "0x10", "0xF0", "0x10", "0xF0",
            "0x90", "0x90", "0xF0", "0x10", "0x10",
            "0xF0", "0x80", "0xF0", "0x10", "0xF0",
            "0xF0", "0x80", "0xF0", "0x90", "0xF0",
            "0xF0", "0x10", "0x20", "0x40", "0x40",
            "0xF0", "0x90", "0xF0", "0x90", "0xF0",
            "0xF0", "0x90", "0xF0", "0x10", "0xF0",
            "0xF0", "0x90", "0xF0", "0x90", "0x90",
            "0xE0", "0x90", "0xE0", "0x90", "0xE0",
            "0xF0", "0x80", "0x80", "0x80", "0xF0",
            "0xE0", "0x90", "0x90", "0x90", "0xE0",
            "0xF0", "0x80", "0xF0", "0x80", "0xF0",
            "0xF0", "0x80", "0xF0", "0x80", "0x80",
        ]
        return fonts