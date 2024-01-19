#!/home/username/parrot/bin/python

class PulseGenerator:
    def __init__(self, pulse_width, amplitude, offset = 0):
        
        self._pulse_width = pulse_width
        self._amplitude = amplitude
        self._offset = offset


    def _even_odd(self, num):
        
        if(int(num)%2 == 0):
            return 1.0
        
        else:
            return -1.0
    

    def generate(self, time):
        
        signal = self._even_odd(time/self._pulse_width)*self._amplitude + self._offset
        return signal