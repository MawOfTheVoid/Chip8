def get_nnn(opcode):
    return opcode & 0x0FFF


def get_x(opcode):
    x = opcode & 0x0F00
    return x >> 8


def get_y(opcode):
    x = opcode & 0x00F0
    return x >> 4


def get_kk(opcode):
    return opcode & 0x00FF


def get_n(opcode):
    return opcode & 0x000F
