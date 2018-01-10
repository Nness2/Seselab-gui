from exn import *

def hw (n):
    return format(n, 'b').count('1')

class Memory:

    def __init__ (self, size):
        self._size = size
        self._mem = [0 for x in range(0, size)]
        self._addr = 0 # address bus
        self._hw = 0 # total Hamming weight
        self._hd = 0 # current cycle Hamming distance

    def __setitem__ (self, addr, val):
        if addr < 0 or addr >= self._size:
            raise AddrError(addr)

        self._hw -= hw(self._mem[addr])
        self._hw += hw(val)

        self._hd += hw(self._mem[addr] ^ val)

        self._addr = addr

        self._mem[addr] = val

    def __getitem__ (self, addr):
        if addr < 0 or addr >= self._size:
            raise AddrError(addr)

        self._addr = addr

        return self._mem[addr]

    def get_activity (self):
        activity = (self._hw // 2) + self._hd + hw(self._addr)
        self._hd = 0
        return activity
