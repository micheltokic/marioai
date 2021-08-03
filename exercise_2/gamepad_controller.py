from inputs import get_gamepad
import math
import threading
from time import sleep
import os


#buttonStatus = {}

class GamepadController (object):
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
        #for b in self.BUTTONS: 
        #    buttonStatus[b] = 0
        self._monitor_thread = threading.Thread(target=self.monitor, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start() 
        
                
    def read(self, env): # return the buttons/triggers that you care about in this methode
        x = self.X
        y = self.Y
        a = self.A
        b = self.B # b=1, x=2
        udp = self.UpDPad
        ddp = self.DownDPad
        rdp = self.RightDPad
        ldp = self.LeftDPad
        return [a, b, x, y, udp, ddp, rdp, ldp]    # TODO: Map to env actions

    def monitor(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LYAXIS = event.state / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LXAXIS = event.state / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RYAXIS = event.state / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RXAXIS = event.state / self.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.SCR_L = event.state / self.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.SCR_R = event.state / self.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.B = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.A = event.state
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
                #elif event.code == 'ABS_HAT0X':
                #    self.RightDPad = event.state
                elif event.code == 'ABS_HAT0Y':
                    if event.state == 1:
                        self.DownDPad = event.state
                    elif event.state == -1:
                        self.UpDPad = event.state
                    else:
                        self.DownDPad = event.state
                        self.UpDPad = event.state
                    #self.UpDPad = event.state
                #elif event.code == 'ABS_HAT0Y':
                #    self.DownDPad = event.state
                #print(event.code)
                

    ########################################################################
    
      #  BUTTONS = [SCR_L, SCR_R, SELECT, START, X, Y, A, B, LeftBumper, RightBumper, LeftThumb, RightThumb, LeftDPad, RightDPad, UpDPad, DownDPad]

       # buttonText = {
       #     SCR_L: "SCR_L",
       #     SCR_R: "SCR_R",
       #     XAXIS: "XAXIS",
       #     YAXIS: "YAXIS",
       #     SELECT: "SELECT",
       #     START: "START",
       #     X: "X",
       #     Y: "Y",
       #     A: "A",
       #     B: "B",
      #      LeftDPad: "LeftDPad",
      #      RightDPad: "RightDPad",
     #       UpDPad: "UpDPad",
     #       DownDPad: "DownDPad"
    #    }
    
      




        
