import pyglet
from emulator import emulator

def start(dt):
    pyglet.clock.schedule_interval(emulator.main, 1/1000)

#need this for pyglet
def update(dt):
    if emulator.cpu.opcode != 0x1210:
        emulator.cpu.cycle()
    else:
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_once(start, 3)

if __name__ == '__main__':
    template = pyglet.gl.Config(double_buffer=True)
    emulator = emulator(640, 320, config=template, caption="Chip-8 emulator")
    emulator.loadROM('IBM.ch8')
    pyglet.clock.schedule(update)
    pyglet.app.run()
