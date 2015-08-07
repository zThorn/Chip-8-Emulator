import cpu
import pyglet


class emulator(pyglet.window.Window):

        def __init__(self, *args, **kwargs):
                super(emulator, self).__init__(*args, **kwargs)
                self.key_map = {pyglet.window.key._1: 0x1,
                                pyglet.window.key._2: 0x2,
                                pyglet.window.key._3: 0x3,
                                pyglet.window.key._4: 0xc,
                                pyglet.window.key.Q: 0x4,
                                pyglet.window.key.W: 0x5,
                                pyglet.window.key.E: 0x6,
                                pyglet.window.key.R: 0xD,
                                pyglet.window.key.A: 0x7,
                                pyglet.window.key.S: 0x8,
                                pyglet.window.key.D: 0x9,
                                pyglet.window.key.F: 0xE,
                                pyglet.window.key.Z: 0xA,
                                pyglet.window.key.X: 0x0,
                                pyglet.window.key.C: 0xB,
                                pyglet.window.key.V: 0xF}
                self.white = pyglet.image.load("pixel.png")
                scip = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 0))
                self.black = scip.create_image(10, 10)
                self.cpu = cpu.CPU(self)
                self.clear()
                self.set_vsync(False)

        def loadROM(self, rompath):
                rom = open(rompath, "rb").read()
                for index in range(0, len(rom)):
                    #Programs by definition start at 0x200, as 0x000->0x200 will be the font file
                    self.cpu.memory[index + 0x200] = rom[index]

        def drawxy(self, x, y):
                if self.cpu.graphics[x][y] == 1:
                        self.white.blit(x*10, 310-y*10)
                else:
                        self.black.blit(x*10, 310 - y *10) 

        def main(self, dt):
                if not self.has_exit:
                    self.dispatch_events()
                    self.cpu.cycle()
