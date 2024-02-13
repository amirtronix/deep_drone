#!/home/username/parrot/bin/python
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0



def new_val(gain: Gains):
    gain.kp = 50

Gain_x = Gains()
Gain_x.kp = 10

print(Gain_x.kp)
new_val(Gain_x)
print(Gain_x.kp)