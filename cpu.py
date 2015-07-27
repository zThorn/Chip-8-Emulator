__author__ = 'zachery.thornton'
import sys
import random
class cpu:
    #Program counter
    def __init__(self):
        #Registers
        self.registers = [0] * 16
        #4k of memory!
        self.memory =  [0]*4096
        #Start the program counter at the start of the program
        self.pc = 0x200
        #Current opcode, gets initialized to 0
        self.opcode = 0

        self.stack = []

        #Also known as I or Index register
        self.address_register = 0

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
        self.pc = self.stack.pop()

    #Jumps to address line NNN (this is passed in by the opcode)
    def op_1NNN(self):
        self.pc = self.opcode & 0x0fff

    def op_2NNN(self):
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    def op_3XNN(self):
        if self.registers[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2

    def op_4XNN(self):
        if self.registers[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def op_5XY0(self):
        if self.registers[self.vx] == self.registers[self.vy]:
            self.pc += 2

    #This should set register at VX == NN
    def op_6XNN(self):
        self.registers[self.vx] = (self.opcode & 0x00ff)

    #This opcode takes in 2 arguments, we're &'ing the opcode with 0x00ff to pull these out'
    def op_7XNN(self):
        self.registers[self.vx] += (self.opcode & 0x00ff)

    def op_8XY0(self):
        self.registers[self.vx] = self.registers[self.vy]

    def op_8XY1(self):
        self.registers[self.vx] = (self.registers[self.vx] | self.registers[self.vy])

    def op_8XY2(self):
        self.registers[self.vx]= (self.registers[self.vx] & self.registers[self.vy])

    def op_8XY3(self):
        self.registers[self.vx]= (self.registers[self.vx] ^ self.registers[self.vy])

#Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
    def op_8XY4(self):
        if (self.registers[self.vx] + self.registers[self.vy]) > 0xff:
            self.registers[0xf] = 1
        else:
            self.registers[0xf] = 0
        self.registers[self.vx] += self.registers[self.vy]

#VY is subtracted from VX ( VX-VY). If there is a borrow, VF is set to 0, else it is set to 1.
    def op_8XY5(self):
        if self.registers[self.vx] - self.registers[self.vy] < 0x0:
            self.registers[0xf] = 0
        else:
            self.registers[0xf] = 1
        self.registers[self.vx] -= self.registers[self.vy]

    # Bit shifts VX right by 1. VF is set to the value of the least significant bit of VX before the shift    
    def op_8XY6(self):
        self.registers[0xf] = self.registers[self.vx] & 0x01
        self.registers[self.vx]  = self.registers[self.vx] >> 1

    #VX is subtracted from VY ( VY-VX). If there is a borrow, VF is set to 0, else it is set to 1.
    def op_8XY7(self):
        if self.registers[self.vy] - self.registers[self.vx] < 0x0:
            self.registers[0xf] = 0
        else:
            self.registers[0xf] = 1
        self.registers[self.vy] -= self.registers[self.vx]

# Bit shifts VX left by 1. VF is set to the value of the least significant bit of VX before the shift    
    def op_8XYE(self):
        self.registers[0xf] = self.registers[self.vx] & 0x01
        self.registers[self.vx]  = self.registers[self.vx] << 1

    #Skips the next instruction if VX != VY
    def op_9XY0(self):
        if self.registers[self.vx] != self.registers[self.vy]:
            self.pc += 2

    #Sets I to the address NNN.
    def op_ANNN(self):
        self.address_register = (self.opcode & 0x0FFF)

    #Jumps to the address NNN plus V0.  Essentially a jmp
    def op_BNNN(self):
        self.pc = (self.opcode & 0x0FFF) + self.registers[0]

    #Sets vx to a random number masked by NN
    def op_CXNN(self):
        self.registers[self.vx] = (random.randint(0x0,0xFF) & (self.opcode & 0x00FF))
        print(self.registers[self.vx])

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