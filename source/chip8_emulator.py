import binascii

class Chip8():

    def __init__(self, rom_path, screen):
        self.rom_path = rom_path
        self.memory = self.prepare_memory()

    def prepare_memory(self):
        memory = self.fonts()
        memory += 4016 * [0]
        memory = self.load_rom(memory)

    def load_rom(self, memory):
        with open(self.rom_path, "rb") as file_obj:
            rom = file_obj.read()
        rom = binascii.hexlify(rom)
        # split rom into two hex values each
        rom = [rom[i:i + 2] for i in range(0, len(rom), 2)]
        # converts them from binary string to normal string
        rom = [hex(int(register, 16)) for register in rom]
        for register in rom:
            print(register)

    def fonts(self):
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