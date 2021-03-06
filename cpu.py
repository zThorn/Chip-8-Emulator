import random

fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
         0x20, 0x60, 0x20, 0x20, 0x70,  # 1
         0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
         0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
         0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
         0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
         0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
         0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
         0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
         0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
         0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
         0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
         0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
         0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
         0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
         0xF0, 0x80, 0xF0, 0x80, 0x80]  # F


class CPU(object):

    def __init__(self, disp):
        #Registers
        self.registers = [0] * 16
        #4k of memory!
        self.memory = [0]*4096
        self.display = disp
        self.graphics = [[0 for x in range(32)] for y in range(64)]
        #Start the program counter at the start of the program
        self.pc = 0x200
        #Current opcode, gets initialized to 0F so python assumes this is a hex #
        self.opcode = 0x0F

        self.stack = []
        self.key_inputs = [0] * 16
        self.delay_timer = 0

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

            0x8000: self.op_8ZZZ,

            0x8FF0: self.op_8XY0,

            0x8FF01: self.op_8XY1,

            0x8FF2: self.op_8XY2,

            0x8FF3: self.op_8XY3,

            0x8FF4: self.op_8XY4,

            0x8FF5: self.op_8XY5,

            0x8FF6: self.op_8XY6,

            0x8FF7: self.op_8XY7,

            0x8FFE: self.op_8XYE,

            0x9000: self.op_9XY0,

            0xA000: self.op_ANNN,

            0xB000: self.op_BNNN,

            0xC000: self.op_CXNN,

            0xD000: self.op_DXYN,

            0xE000: self.op_EZZZ,

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
        self.lookupOP(self.opcode & 0xf000)

    def _get_key(self):
        for index in range(16):
            if self.key_inputs[index] == 1:
                return index
        return -1

    def lookupOP(self, op):
        try:
            #Get the appropriate opcode's function, and execute
            func = self.INSTRUCTION_SET[op]
            func()
        except Exception as e:
            print(e)
            print(format(op,"02x"))

######################
######OPERATIONS######
######################
    def op_0ZZZ(self):
        self.lookupOP(self.opcode & 0xf0ff)
    
    def op_00E0(self):
        self.graphics = [[0 for x in range(32)] for y in range(64)]
        self.display.clear()
        self.display.flip()
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

    def op_8ZZZ(self):
        self.lookupOP((self.opcode & 0xf00f) + 0xff0)

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

    def op_DXYN(self):
        #draws sprites
        x = self.registers[self.vx] & 0xff
        y = self.registers[self.vy] & 0xff
        height = self.opcode & 0x000f
        self.registers[0xf] = 0
        for y_offset in range(height):
            current_row = self.memory[y_offset + self.address_register]
            for x_offset in range(8):
                if y + y_offset >= 32 or (x + x_offset) >= 64:
                    continue
                if current_row & (0x80 >> x_offset) != 0:
                    if self.graphics[x + x_offset][y + y_offset]:
                        self.registers[0xf] = 1
                    self.graphics[x + x_offset][y + y_offset] ^= 1
                    self.display.drawxy(x + x_offset, y + y_offset)
        self.display.flip()

    def op_EX9E(self):
        # Skips the next instruction if the key stored in VX is pressed
        key = self.registers[self.vx] & 0xf
        if self.key_inputs[key] == 1:
            self.pc += 2

    def op_EXA1(self):
        # Skips the next instruction if the key stored in VX isn't pressed
        key = self.registers[self.vx] & 0xf
        if self.key_inputs[key] == 0:
            self.pc += 2

    def op_EZZZ(self):
        self.lookupOP(self.opcode & 0xf0ff)

    def op_FX07(self):
        # Sets VX to the value of the delay timer
        self.registers[self.vx] = self.delay_timer

    def op_FX0A(self):
        # A key press is awaited, and then stored in VX
        ret = self._get_key()
        if ret >= 0:
            self.registers[self.vx] = ret
        else:
            self.pc -= 2

    def op_FX15(self):
        # Sets the delay timer to VX
        self.delaytimer = self.registers[self.vx]

    def op_FX18(self):
        #Set sound timer to VX
        self.sound_timer = self.registers[self.vx]

    def op_FX1E(self):
        #Adds VX to I, If overflow, VF = 1
        self.address_register += self.registers[self.vx]
        if self.address_register > 0xfff:
            self.registers[0xf] = 1
            self.address_register &= 0xfff
        else:
            self.registers[0xf] = 0

    def op_FX29(self):
        #sets I to the location of the sprite for the character in VX.
        self.address_register = (5 * (self.registers[self.vx])) & 0xfff

    def op_FX33(self):
        #store a number as BCD(Binary Coded Decimal)
        self.memory[self.address_register] = int(self.registers[self.vx] / 100)
        self.memory[self.address_register + 1] = int(self.registers[self.vx] / 10) % 10
        self.memory[self.address_register + 2] = (self.registers[self.vx] % 10)

    def op_F055(self):
        #stores V0 to VX in memory starting at address I
        for index in range(0, self.vx + 1):
            self.memory[self.address_register + index] = self.registers[index]

    def op_FX65(self):
        #stores V0 to VX with values from memory starting at address I
        for index in range(0, self.vx + 1):
            self.registers[index] = self.memory[self.address_register + index]

    def op_FZZZ(self):
            self.lookupOP(self.opcode & 0xf0ff)

