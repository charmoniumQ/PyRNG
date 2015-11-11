#!/usr/bin/env python3
class LFSR:
    def __init__(self, seed, taps):
        self.seed(seed)
        self.taps(taps)
        for x in self.taps:
            if x > len(self.seed):
                raise RuntimeError('Tried to tap a nonexistent bit')

    def seed(self, seed):
        if type(seed) is int:
            self.seed = list(map(int, str(seed)))
            self.contains = 'int'
        elif type(seed) is str:
            self.seed = list(seed)
            self.contains = 'str'
        else:
            raise RuntimeError('Unexpected Seed Input')
        
    def taps(self, taps):
        if type(taps) is list:
            self.taps = taps
        else:
            raise RuntimeError('Taps type should be list')
    
    def next(self):
        self.hide_seed()
        if self.contains == 'str':
            self.iterate_string()
            return self.output
        elif self.contains == 'int':
            self.iterate_integer()
            return self.output
        else:
            raise RuntimeError('Unexpected Seed Input')

    def hide_seed(self):
        if self.contains == 'str':
            for x in range (1, len(self.seed) + 1):
                self.iterate_string()
        elif self.contains == 'int':
            for x in range (1, len(self.seed) + 1):
                self.iterate_integer()
        else:
            raise RuntimeError('Unexpected Seed Input')

    def iterate_string(self):
        if self.contains == "str":
            self.output = self.seed[len(self.seed) - 1]
            xor = ord(self.seed[self.taps[0] - 1])
            for x in range(1, len(self.taps)):
                xor = xor ^ ord(self.seed[self.taps[x] - 1])
            for x in range(1,len (self.seed) + 1):
                self.seed[len(self.seed) - x] = self.seed[len(self.seed) - x - 1]
            self.seed[0] = chr(xor)
        else:
            raise RuntimeError("Can't call on non-string list")
        
    def iterate_integer(self):
        if self.contains == "int":
            self.output = self.seed[len(self.seed) - 1]
            xor = self.seed[self.taps[0] - 1]
            for x in range(1, len(self.taps)):
                xor = xor ^ self.seed[self.taps[x] - 1]
            for x in range(1, len(self.seed) + 1):
                self.seed[len(self.seed) - x] = self.seed[len(self.seed) - x - 1]
            self.seed[0] = xor
            return output
        else:
            raise RuntimeError("Can't call on non-integer list")

    def state(self):
        return self.seed

    def display(self):
        print(self.seed)
        tapsdisplay = '['
        for x in range(1, len(self.seed) + 1):
            if x in self.taps:
                tapsdisplay += 'T, '
            else:
                tapsdisplay += ' , '
        tapsdisplay = tapsdisplay[:-2]
        tapsdisplay += "]"
        print(tapsdisplay)

x = LFSR("ABCEFGH", [5])
for y in range(0, 20):
    print(x.next())
x.display()
