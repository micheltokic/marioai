from inputs import get_gamepad
import math
import threading
import gym
from gym_marioai import levels
import keyboard


# buttonStatus = {}

class Gamepad_Mario_Play(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    all_actions = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    env = gym.make('Marioai-v0', render=True,
                   level_path=levels.one_cliff_level,
                   compact_observation=True,
                   enabled_actions=all_actions,
                   rf_width=20, rf_height=10)

    def __init__(self):
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

    def read(self):  # return the buttons/triggers that you care about in this methode
        x = self.X
        y = self.Y
        a = self.A
        b = self.B  # b=1, x=2
        udp = self.UpDPad
        ddp = self.DownDPad
        rdp = self.RightDPad
        ldp = self.LeftDPad
        rb = self.RightBumper
        lb = self.LeftBumper
        return [a, b, x, y, udp, ddp, rdp, ldp, rb, lb]

    def monitor(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LYAXIS = event.state / Gamepad_Mario_Play.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LXAXIS = event.state / Gamepad_Mario_Play.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RYAXIS = event.state / Gamepad_Mario_Play.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RXAXIS = event.state / Gamepad_Mario_Play.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.SCR_L = event.state / Gamepad_Mario_Play.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.SCR_R = event.state / Gamepad_Mario_Play.MAX_TRIG_VAL  # normalize between 0 and 1
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

    def get_action(self):
        if (keyboard.is_pressed('shift+space+right')) or (self.RightDPad == 1 and self.B == 1 and self.A ==1):
            return Gamepad_Mario_Play.env.SPEED_JUMP_RIGHT
        if keyboard.is_pressed('shift+space+left') or (self.LeftDPad == -11 and self.B == 1 and self.A ==1):
            return Gamepad_Mario_Play.env.SPEED_JUMP_LEFT

        elif keyboard.is_pressed('space+right') or (self.RightDPad == 1 and self.A ==1):
            return Gamepad_Mario_Play.env.JUMP_RIGHT
        elif keyboard.is_pressed('space+left') or (self.LeftDPad == -1 and self.A ==1):
            return Gamepad_Mario_Play.env.JUMP_LEFT

        if keyboard.is_pressed('shift+right') or (self.RightDPad == 1 and self.B ==1):
            return Gamepad_Mario_Play.env.SPEED_RIGHT
        if keyboard.is_pressed('shift+left') or (self.LeftDPad == -1 and self.B ==1):
            return Gamepad_Mario_Play.env.SPEED_LEFT

        elif keyboard.is_pressed('right') or (self.RightDPad == 1):
            return Gamepad_Mario_Play.env.RIGHT
        elif keyboard.is_pressed('left') or (self.LeftDPad == -1):
            return Gamepad_Mario_Play.env.LEFT
        elif keyboard.is_pressed('down') or (self.DownDPad == 1):
            return Gamepad_Mario_Play.env.DOWN
        elif keyboard.is_pressed('space') or (self.A == 1):
            return Gamepad_Mario_Play.env.JUMP
        else:
            return Gamepad_Mario_Play.env.NOTHING



if __name__ == '__main__':
    joy = Gamepad_Mario_Play()
    events = get_gamepad()
    while True:
        s = Gamepad_Mario_Play.env.reset()
        done = False
        total_reward = 0

        while not done:
            a = Gamepad_Mario_Play.get_action()
            print('action', a)
            s, r, done, info = Gamepad_Mario_Play.env.step(a)
            # print(len(s), ':', s)

            total_reward += r

        print(f'finished episode, total_reward: {total_reward}')

    print('finished demo')

