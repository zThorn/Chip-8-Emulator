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
		print("1NNN Success!")
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
		print("3XNN Success!")

	def test4XNN(self):
		#Configure the variables to values that make sense
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x21
		self.testCPU.opcode = 0x0022
		self.testCPU.pc = 0

		self.testCPU.op_4XNN()

		self.assertEqual(self.testCPU.pc,2)
		print("4XNN Success!")

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
		print("5XY0 Success!")

	def test6XNN(self):
		self.testCPU.opcode = 0x3F31
		self.testCPU.vx = 0

		self.testCPU.op_6XNN()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx],0x31)
		print("6XNN Success!")

	def test7XNN(self):
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x20
		self.testCPU.opcode = 0x1120
		self.testCPU.op_7XNN()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx],0x40)
		print("7XNN  success!")

	def test8XY0(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vy] = 0x25

		self.testCPU.op_8XY0()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx], 0x25)
		print("8XY0 success!")
	def test8XY1(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x20
		self.testCPU.registers[self.testCPU.vy] = 0x25

		self.testCPU.op_8XY1()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx], 0x25)
		print("8XY1 success!")

	def test8XY2(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x20
		self.testCPU.registers[self.testCPU.vy] = 0x25

		self.testCPU.op_8XY2()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx], 0x20)
		print("8XY2 success!")
	
	def test8XY3(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x20
		self.testCPU.registers[self.testCPU.vy] = 0x25

		self.testCPU.op_8XY3()
		self.assertEqual(self.testCPU.registers[self.testCPU.vx], 0x5)
		print("8XY3 success!")

	def test8XY4(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0xFF
		self.testCPU.registers[self.testCPU.vy] = 0x1

		self.testCPU.op_8XY4()
		self.assertEqual(self.testCPU.registers[0xf],1)

		self.testCPU.registers[self.testCPU.vx] = 0xFE
		self.testCPU.registers[self.testCPU.vy] = 0x01

		self.testCPU.op_8XY4()
		self.assertEqual(self.testCPU.registers[0xf],0)
		print("8XY4 success!")

	def test8XY5(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x0
		self.testCPU.registers[self.testCPU.vy] = 0x1

		self.testCPU.op_8XY5()
		self.assertEqual(self.testCPU.registers[0xf],0)

		self.testCPU.registers[self.testCPU.vx] = 0x1
		self.testCPU.registers[self.testCPU.vy] = 0x0
		self.testCPU.op_8XY5()
		self.assertEqual(self.testCPU.registers[0xf],1)
		print("8XY5 success!")

	def test8XY6(self):
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0xF1
		self.testCPU.op_8XY6()
		self.assertEqual(self.testCPU.registers[0xf],1)
		self.assertEqual(self.testCPU.registers[self.testCPU.vx],0x78)
		print("8XY6 success!")

	def test8XY7(self):
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x1
		self.testCPU.registers[self.testCPU.vy] = 0x0

		self.testCPU.op_8XY7()
		self.assertEqual(self.testCPU.registers[0xf],0)

		self.testCPU.registers[self.testCPU.vx] = 0x0
		self.testCPU.registers[self.testCPU.vy] = 0x1

		self.testCPU.op_8XY7()
		self.assertEqual(self.testCPU.registers[0xf],1)
		print("8XY7 success!")


	def test8XYE(self):
		self.testCPU.vx = 0
		self.testCPU.registers[self.testCPU.vx] = 0x01
		self.testCPU.op_8XYE()
		self.assertEqual(self.testCPU.registers[0xf],1)
		self.assertEqual(self.testCPU.registers[self.testCPU.vx],0x02)
		print("8XYE success!")

	def test9XY0(self):
		self.testCPU.pc = 0
		self.testCPU.vx = 0
		self.testCPU.vy = 1
		self.testCPU.registers[self.testCPU.vx] = 0x1
		self.testCPU.registers[self.testCPU.vy] = 0x0

		self.testCPU.op_9XY0()
		self.assertEqual(self.testCPU.pc, 2)

		self.testCPU.registers[self.testCPU.vx] = 0x0
		self.testCPU.op_9XY0()
		self.assertEqual(self.testCPU.pc,2)
		print("9XY0 success!")

	def testANNN(self):
		self.testCPU.opcode = 0xAE1E

		self.testCPU.op_ANNN()
		self.assertEqual(self.testCPU.address_register,0xE1E)
		print("ANNN success!")

	def testBNNN(self):
		self.testCPU.registers[0] = 0x1
		self.testCPU.opcode = 0xF111

		self.testCPU.op_BNNN()
		self.assertEqual(self.testCPU.pc, 0x112)
		print("BNNN success!")

	#Theres really no good way to unit test a random number generator....
	#Ive checked to make sure this does return different numbers, im leaving this
	#in for no good reason.
	def testCXNN(self):
		self.testCPU.opcode = 0x0011
		self.testCPU.op_CXNN()



#Add the appropriate unit test call here!
test = Chip8Tests()
#This should only be called once, its to initialize the environment
test.setUp()
test.test1NNN()
test.test3XNN()
test.test4XNN()
test.test5XY0()
test.test6XNN()
test.test7XNN()
test.test8XY0()
test.test8XY1()
test.test8XY2()
test.test8XY3()
test.test8XY4()
test.test8XY5()
test.test8XY6()
test.test8XY7()
test.test8XYE()
test.test9XY0()
test.testANNN()
test.testBNNN()
#Destroys the test CPU object
test.tearDown()