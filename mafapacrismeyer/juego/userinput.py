from pygame import key

class UserInput:
    def __init__(self):
        self._input = [0, 0, 0, 0]

    def get_input(self):
        return self._input    
    
    def update(self):
        keyboard = key.get_pressed()
        if keyboard[97]: # a
            Xinput = -1
        elif keyboard[100]: # d
            Xinput = 1
        else:
            Xinput = 0
            
        if keyboard[119]: # w
            Yinput = 1
        elif keyboard[115]: # s
            Yinput = -1
        else:
            Yinput = 0

        if keyboard[32]: # SPACE
            jumpInput = 1
        else:
            jumpInput = 0
            
        if keyboard[109]: # m
            actionInput = 1
        else:
            actionInput = 0

        self._input[0] = Xinput
        self._input[1] = Yinput
        self._input[2] = jumpInput
        self._input[3] = actionInput
