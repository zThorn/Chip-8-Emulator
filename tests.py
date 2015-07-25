import cpu
import unittest

class Chip8Tests(unittest.TestCase):

	def setUp(self):
		self.testCPU = cpu.cpu()

	def tearDown(self):
		self.testCPU = None

	def test1NNN(self):
		#REMEMBER TO ALWAYS USE HEX
		self.testCPU.opcode = 0x1222
		self.testCPU.op_1NNN()
		#0x222h == 546d
		self.assertEqual(self.testCPU.pc,0x222)

	def test3XNN(self):
		#Configure the variables to values that make sense
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x22
		self.testCPU.opcode = 0x0022
		self.testCPU.pc = 0

		#Call the opcode!
		self.testCPU.op_3XNN()

		#Assert that the values make sense!
		self.assertEqual(self.testCPU.pc,2)

	def test4XNN(self):
		#Configure the variables to values that make sense
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x21
		self.testCPU.opcode = 0x0022
		self.testCPU.pc = 0

		self.testCPU.op_4XNN()

		self.assertEqual(self.testCPU.pc,2)

	def test5XY0(self):
		#Configure the variables to values that make sense
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x21
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vy] = 0x21
		self.testCPU.opcode = 0x0022
		self.testCPU.pc = 0

		self.testCPU.op_5XY0()

		self.assertEqual(self.testCPU.pc,2)

#Add the appropriate unit test call here!
test = Chip8Tests()
#This should only be called once, its to initialize the environment
test.setUp()
test.test1NNN()
test.test3XNN()
test.test4XNN()
test.test5XY0()
#Destroys the test CPU object
test.tearDown()