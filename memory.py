"""
Simulated RAM
"""
import struct
from constants import TYPE_TO_SIZE, TYPE_TO_STRUCT


class VMMemory(object):
    """
    Word-indexed memory (4-byte words)
    """
    def __init__(self, size):
        self.size = size
        self._data = [struct.pack('>i', 0)]*size

    def store_4(self, idx, word):
        assert(type(word) == str)
        assert(len(word) == 4)
        self._data[idx] = word

    def read_4(self, idx):
        return self._data[idx]

    def store_8(self, idx, word):
        assert(type(word) == str)
        assert(len(word) == 8)
        self._data[idx] = word[0:4]
        self._data[idx+1] = word[4:8]

    def read_8(self, idx):
        w1 = self._data[idx]
        w2 = self._data[idx+1]
        return w1+w2

    def store(self, type, idx, num):
        s = struct.pack(TYPE_TO_STRUCT[type], num)
        size = TYPE_TO_SIZE[type]
        if size == 4:
            self.store_4(idx, s)
        else:
            self.store_8(idx, s)

    def read(self, type, idx):
        size = TYPE_TO_SIZE[type]
        if size == 4:
            s = self.read_4(idx)
        else:
            s = self.read_8(idx)
        return struct.unpack(TYPE_TO_STRUCT[type], s)[0]

    def __repr__(self):
        msg = '['
        for idx in range(self.size):
            value = self._data[idx]
            msg += str(struct.unpack('>i', value)[0])+' ,'
        msg += ']'
        return msg