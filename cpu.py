__author__ = 'zachery.thornton'
import sys

class cpu:
    #Program counter
    def __init__(self):
        #Registers
        self.registers = bytearray(16)
        #4k of memory!
        self.memory =  [0]*4096
        #Start the program counter at the start of the program
        self.pc = 0x200
        #Current opcode, gets initialized to 0
        self.opcode = 0

        self.stack = []

        ## This is a list of all chip-8 instructions.
        ## In order to implement a chip-8 fxn, simply name your
        ## function after the opcode you are attempting to implement
        ##
        self.INSTRUCTION_SET = {
            0x0000: self.op_0ZZZ,
            0x00E0: self.op_00E0,
            0x00EE: self.op_00EE,
            0x1000: self.op_1NNN,
            0x2000: self.op_2NNN,
            0x3000: self.op_3XNN,
            0x4000: self.op_4XNN,
            0x5000: self.op_5XY0,
            0x6000: self.op_6XNN,
            0x7000: self.op_7XNN,
            0x8000: self.op_8XY0,
            0x8001: self.op_8XY1,
            0x8002: self.op_8XY2,
            0x8003: self.op_8XY3,
            0x8004: self.op_8XY4,
            0x8005: self.op_8XY5,
            0x8006: self.op_8XY6,
            0x8007: self.op_8XY7,
            0x800E: self.op_8XYE,
            0x9000: self.op_9XY0,
            0xA000: self.op_ANNN,
            0xB000: self.op_BNNN,
            0xC000: self.op_CXNN,
            0xD000: self.op_DXYN,
            0xE09E: self.op_EX9E,
            0xE0A1: self.op_EXA1,
            0xF000: self.op_FZZZ,
            0xF007: self.op_FX07,
            0xF00A: self.op_FX0A,
            0xF015: self.op_FX15,
            0xF018: self.op_FX18,
            0xF01E: self.op_FX1E,
            0xF029: self.op_FX29,
            0xF033: self.op_FX33,
            0xF055: self.op_F055,
            0xF065: self.op_FX65,
        }

    def dumpregs(self):
        print("##########")
        print("#VX  =  {0}").format(self.vx)
        print("#VY  =  {0}").format(self.vy)
        print("##########")
        print(self.registers)

    #Consider this the "Update Loop"
    def cycle(self):

        self.opcode = (self.memory[self.pc] << 8) | (self.memory[self.pc + 1])
        #Forward the program counter
        self.pc += 2
        #Pull out VX & VY
        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4

        #Decode the opcode from memory
        extracted_op = self.opcode & 0xf000

        try:
            #Get the appropriate opcode's function, and execute
            func = self.INSTRUCTION_SET[extracted_op]
            func()
        except Exception as e:
            print("Undefined opcode: "+str(self.opcode))


    def loadROM(self, rompath):
        rom = open(rompath, "rb").read()
        for index in range(0, len(rom)):
            #Programs by definition start at 0x200, as 0x000->0x200 will be the font file
            self.memory[index + 0x200] = rom[index]


######################
######OPERATIONS######
######################
    def op_0ZZZ(self):
        return
    def op_00E0(self):
        print("00E0")

    #Returns from a subroutine, essentially a return statement
    def op_00EE(self):
        print("00EE")
        self.pc = self.stack.pop()

    #Jumps to address line NNN (this is passed in by the opcode)
    def op_1NNN(self):
        self.pc = self.opcode & 0x0fff

    def op_2NNN(self):
        print("2NNN")
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    def op_3XNN(self):
        print("3XNN")
        if self.registers[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2

    def op_4XNN(self):
        print("4XNN")
        if self.registers[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def op_5XY0(self):
        print("5XY0")
        if self.registers[self.vx] == self.registers[self.vy]:
            self.pc += 2

    def op_6XNN(self):
        print("6XNN")
        self.registers[self.vx] = (self.opcode & 0x00ff)

    def op_7XNN(self):
        #This opcode takes in 2 arguments, we're &'ing the opcode with 0x00ff to pull these out'
        print("7XNN")
        self.registers[self.vx] + (self.opcode & 0x00ff)

    def op_8XY0(self):
        print("8XY0")
        self.registers[self.vx] = self.registers[self.vy]

    def op_8XY1(self):
        print("8XY1")
        self.registers[self.vx] = (self.registers[self.vx] | self.registers[self.vy])

    def op_8XY2(self):
        print("8XY2")
        self.registers[self.vx]= (self.registers[self.vx] & self.registers[self.vy])

    def op_8XY3(self):
        print("8XY3")
        self.registers[self.vx]= (self.registers[self.vx] ^ self.registers[self.vy])

    def op_8XY4(self):
        print("8XY4")

    def op_8XY5(self):
        print("8XY5")

    def op_8XY6(self):
        print("8XY6")

    def op_8XY7(self):
        print("8XY7")

    def op_8XYE(self):
        print("8XYE")

    def op_9XY0(self):
        print("9XY0")

    def op_ANNN(self):
        print("ANNN")

    def op_BNNN(self):
        print("BNNN")

    def op_CXNN(self):
        print("CXNN")

    def op_DXYN(self):
        print("DXYN")

    def op_EX9E(self):
        print("EX9E")

    def op_EX93(self):
        print("EX93")

    def op_EXA1(self):
        print("EXA1")

    def op_FX07(self):
        print("FX07")

    def op_FX0A(self):
        print("FX0A")

    def op_FX15(self):
        print("FX15")

    def op_FX18(self):
        print("FX18")

    def op_FX1E(self):
        print("FX1E")

    def op_FX29(self):
        print("FX29")

    def op_FX33(self):
        print("FX33")

    def op_F055(self):
        print("F055")

    def op_FX65(self):
        print("FX65")

    def op_FZZZ(self):
        print("FZZZ")

    def main(self):
        self.loadROM(sys.argv[1])
        self.opcode=0
        #This should error out once the mem limit is hit, for obv reasons
        while(True):
            self.cycle()

#chip8 = cpu()
#chip8.main()