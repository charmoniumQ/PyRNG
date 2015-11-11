#!/usr/bin/env python3
import itertools

#### Object-oriented LFSR
class LFSRClass:
    def __init__(self, seed, taps, tapfunc=None):
        self.seed = seed
        self.taps = taps
        if tapfunc is None:
            self.tapfunc = default_tapfunc

    def setSeed(self, seed):
        # self._seed is the actual seed
        if isinstance(seed, int):
            self._seed = list(map(int, str(seed)))
        else:
            # http://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
            try:
                self._seed = list(iter(seed))
            except TypeError: # this TypeError exception says 'not an iterator'
                # I want one that says something else
                raise TypeError('Seed must be an integer or an iterable')

    def getSeed(self):
        return self._seed

    # self.seed is what it it appears to the outside
    seed = property(getSeed, setSeed)

    def setTaps(self, taps):
        for tap in taps:
            if tap >= len(self.seed):
                raise RuntimeError('Tried to tap non-existant bit')
        self._taps = taps

    def getTaps(self):
        return self._taps

    taps = property(getTaps, setTaps)

    def __iter__(self):
        # returns an iterable
        # conveniently, self is an iterable
        return self

    def __next__(self):
        a = self.seed[0]
        b = 0
        for tap in self.taps:
            b = self.tapfunc(b, self.seed[tap])
        # shift everything down by one
        self.seed[:-1] = self.seed[1:]
        self.seed[-1] = b
        return a

    def display(self):
        output = [' '] * len(self.seed)
        for tap in self.taps:
            output[tap] = 'T'
        return ', '.join(output)

def demo1():
    a = LFSRClass([1, 0, 0, 0], [0, 1])
    for n, r in zip(range(10), a):
        # get the first ten results
        print('{0}: {1}'.format(n, r))
    print()
    a = LFSRClass(map(int, '1000'), [0, 1])
    ctr = 0
    for r in itertools.islice(a, 10):
        # another way to get the ten
        print('{0}: {1}'.format(ctr, r))

##### Generator based LFSR
def LFSRFunction(seed, taps, tapfunc=None):
    # not so object oriented
    if isinstance(seed, int):
        seed = map(int, str(seed))
    else:
        # http://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
        try:
            seed = list(iter(seed))
        except TypeError: # this TypeError exception says 'not an iterator'
            # I want one that says something else
            raise TypeError('Seed must be an integer or an iterable')

    if tapfunc == None:
        tapfunc = default_tapfunc

    while True:
        a = seed[0]
        b = 0
        for tap in taps:
            b = tapfunc(b, seed[tap])
        seed[:-1] = seed[1:]
        seed[-1] = b
        yield a

def LFSRDisplay(taps, n):
    output = [' '] * n
    for tap in self.taps:
        output[tap] = 'T'
    return ', '.join(output)

def demo2():
    a = LFSRFunction([1, 0, 0, 0], [0, 1])
    ctr = 0
    for r in a:
        print('{ctr}: {r}'.format(ctr=ctr, r=r))
        ctr += 1
        if ctr >= 10:
            break
    print()
    a = LFSRFunction([1, 0, 0, 0], [0, 1])
    for n, r in zip(range(10), a):
        print('{n}: {r}'.format(**locals()))


###### Helper function
def default_tapfunc(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a ^ b
    if isinstance(a, str) and isinstance(b, str):
        return chr(ord(a) ^ ord(b))
    raise TypeError("The default tap function doesn't know how to xor the types: {0!s} and {1!s}".format(type(a), type(b)))
