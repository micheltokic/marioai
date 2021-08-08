from inputs import get_gamepad
import math
import threading
import gym
from gym_marioai import levels
import keyboard


# buttonStatus = {}

class GamepadController:
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)


    def __init__(self, env):
        self.env = env
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        # for b in self.BUTTONS:
        #    buttonStatus[b] = 0
        self._monitor_thread = threading.Thread(target=self.monitor, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def monitor(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LYAXIS = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LXAXIS = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RYAXIS = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RXAXIS = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.SCR_L = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.SCR_R = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.B = event.state  # Snes controller hat unten B
                elif event.code == 'BTN_NORTH':
                    self.X = event.state  # Snes controller hat oben X
                elif event.code == 'BTN_WEST':
                    self.Y = event.state  # Snes controller hat links Y
                elif event.code == 'BTN_EAST':
                    self.A = event.state  # Snes controller hat rechts A
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.SELECT = event.state
                elif event.code == 'BTN_START':
                    self.START = event.state
                elif event.code == 'ABS_HAT0X':
                    if event.state == -1:
                        self.LeftDPad = event.state
                    elif event.state == 1:
                        self.RightDPad = event.state
                    else:
                        self.LeftDPad = event.state
                        self.RightDPad = event.state
                elif event.code == 'ABS_HAT0Y':
                    if event.state == 1:
                        self.DownDPad = event.state
                    elif event.state == -1:
                        self.UpDPad = event.state
                    else:
                        self.DownDPad = event.state
                        self.UpDPad = event.state

    def read(self):
        if (self.RightDPad == 1 and self.B == 1 and self.A == 1):
            return self.env.SPEED_JUMP_RIGHT
        if (self.LeftDPad == -1 and self.B == 1 and self.A == 1):
            return self.env.SPEED_JUMP_LEFT

        elif (self.RightDPad == 1 and self.B == 1):
            return self.env.JUMP_RIGHT
        elif (self.LeftDPad == -1 and self.B == 1):
            return self.env.JUMP_LEFT

        if (self.RightDPad == 1 and self.A == 1):
            return self.env.SPEED_RIGHT
        if (self.LeftDPad == -1 and self.A == 1):
            return self.env.SPEED_LEFT

        elif (self.RightDPad == 1):
            return self.env.RIGHT
        elif (self.LeftDPad == -1):
            return self.env.LEFT
        elif (self.DownDPad == 1):
            return self.env.DOWN
        elif (self.B == 1):
            return self.env.JUMP
        else:
            return self.env.NOTHING


