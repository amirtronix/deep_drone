#!/home/username/parrot/bin/python

from collections import namedtuple

Gains = namedtuple('Gains', 'x, y, z')




class PidController:
    def __init__(self, _gains, _sample_time, _anti_windup=None):
        
        self.gains = Gains(0, 0, 0)
        self._setGains(_gains)
        self._ts = _sample_time


    def _setGains(self, _gains_list):
        self.gains = Gains(_gains_list[0], _gains_list[1], _gains_list[2])

    def _antiWindup(self):
        pass

    def _cmd_sat(self):
        pass

    def _integral(self, error):
        return 0

    def _derivateive(self, error):
        return 0
    
    def compute(self, error):
        _contorlSignal = self.gains[0]*error + \
            self.gains[1]*self._integral(error) + \
            self.gains[1]*self._derivateive(error)


controller = PidController()