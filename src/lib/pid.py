#!/home/accurpress/parrot/bin/python
from collections import namedtuple

Gains = namedtuple('Gains', 'x, y, z')




class PidController:
    def __init__(self, _gains, _sample_time=None, _anti_windup=None):
        
        self.gains = Gains(0, 0, 0)
        self._setGains(_gains)


    def _setGains(self, _gains_list):
        self.gains = Gains(_gains_list[0], _gains_list[1], _gains_list[2])

    def _antiWindup(self):
        pass

    def _cmd_sat(self):
        pass

    def compute(self):
        pass


controller = PidController()