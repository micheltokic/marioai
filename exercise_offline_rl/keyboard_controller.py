import keyboard


class KeyboardController:
    def __init__(self, env):
        self.env = env

    def read(self):
        if keyboard.is_pressed('A+S+right'):
            return self.env.SPEED_JUMP_RIGHT
        elif keyboard.is_pressed('A+S+left'):
            return self.env.SPEED_JUMP_LEFT
        elif keyboard.is_pressed('S+right'):
            return self.env.JUMP_RIGHT
        elif keyboard.is_pressed('S+left'):
            return self.env.JUMP_LEFT
        elif keyboard.is_pressed('A+right'):
            return self.env.SPEED_RIGHT
        elif keyboard.is_pressed('A+left'):
            return self.env.SPEED_LEFT
        elif keyboard.is_pressed('right'):
            return self.env.RIGHT
        elif keyboard.is_pressed('left'):
            return self.env.LEFT
        elif keyboard.is_pressed('down'):
            return self.env.DOWN
        elif keyboard.is_pressed('S'):
            return self.env.JUMP
        else:
            return self.env.NOTHING
