import struct
from constants import TYPE_TO_SIZE, TYPE_TO_STRUCT


class VMStack(object):
    def __init__(self):
        # Stack of 4-byte words
        self._stack = []

    def push_4(self, word):
        assert(type(word) == str)
        assert(len(word) == 4)
        self._stack.append(word)

    def pop_4(self):
        return self._stack.pop()

    def peek_4(self):
        return self._stack[-1]

    def push_8(self, word):
        assert(type(word) == str)
        assert(len(word) == 8)
        self._stack.append(word[0:4])
        self._stack.append(word[4:8])

    def pop_8(self):
        w1 = self._stack.pop()
        w2 = self._stack.pop()
        return w2+w1

    def peek_8(self):
        w1 = self._stack[-1]
        w2 = self._stack[-2]
        return w2+w1

    def push(self, type, num):
        s = struct.pack(TYPE_TO_STRUCT[type], num)
        size = TYPE_TO_SIZE[type]
        if size == 4:
            self.push_4(s)
        else:
            self.push_8(s)

    def pop(self, type):
        size = TYPE_TO_SIZE[type]
        if size == 4:
            s = self.pop_4()
        else:
            s = self.pop_8()
        return struct.unpack(TYPE_TO_STRUCT[type], s)[0]

    def peek(self, type):
        size = TYPE_TO_SIZE[type]
        if size == 4:
            s = self.peek_4()
        else:
            s = self.peek_8()
        return struct.unpack(TYPE_TO_STRUCT[type], s)[0]

    def clone(self, top_bytes=0):
        new_stack = VMStack()
        new_stack._stack = self._stack[-top_bytes:]
        return new_stack

    def __repr__(self):
        limit = min(20, len(self._stack))
        msg = '['
        if len(self._stack) > 20:
            msg += '...'

        for idx in range(len(self._stack)-limit, len(self._stack)):
            value = self._stack[idx]
            msg += ' '+str(struct.unpack('>i', value)[0])
        msg += ']'
        return msg


if __name__ == "__main__":
    stack = VMStack()
    stack.push('i', 356)
    stack.push('l', 3101202303)
    print stack.pop('l') == 3101202303
    print stack.pop('i') == 356

    stack.push('f', 356)
    stack.push('d', 3101202303)
    stack2 = stack.clone(top_bytes=12)

    print stack2.pop('d') == 3101202303
    print stack2.pop('f') == 356

    print stack.pop('l') == 4748794100233273344
    print stack.pop('i') == 1135738880