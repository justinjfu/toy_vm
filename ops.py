"""
Implementations of instructions
"""

class BTZInst(object):
    def __init__(self):
        pass

    def execute(self, thread):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__


class BTZNop(BTZInst):
    def execute(self, thread):
        thread.state.pc += 1


class BTZExit(BTZInst):
    def execute(self, thread):
        if thread.state.alive:
            thread.state.alive = False
            thread.runtime.command_kill_thread(thread.id)
        else:
            raise ValueError('Thread already dead: '+thread.id)


class BTZSpawnThread(BTZInst):
    def __init__(self, top_bytes, pc_offset):
        super(BTZSpawnThread, self).__init__()
        self.top_bytes = top_bytes
        self.pc_offset = pc_offset
        assert pc_offset != 0  # Offset=0 creates an infinite loop

    def execute(self, thread):
        new_stack = thread.state.stack.clone(top_bytes=self.top_bytes)
        thread.runtime.command_spawn_thread(new_stack, thread.state.pc+self.pc_offset)
        thread.state.pc += 1


class BTZBinaryOp(BTZInst):
    def __init__(self, type, op):
        super(BTZBinaryOp, self).__init__()
        self.op = op
        self.type = type

    def execute(self, thread):
        b = thread.state.stack.pop(self.type)
        a = thread.state.stack.pop(self.type)
        thread.state.stack.push(self.type, self.op(a,b))
        thread.state.pc += 1

    def __repr__(self):
        return '%s_%s' % (self.op.__name__, self.type)


class BTZPush(BTZInst):
    def __init__(self, type, value):
        super(BTZPush, self).__init__()
        self.value = value
        self.type = type

    def execute(self, thread):
        thread.state.stack.push(self.type, self.value)
        thread.state.pc += 1

    def __repr__(self):
        return 'push_%s:%s' % (self.type, self.value)


class BTZPop(BTZInst):
    def __init__(self, type):
        super(BTZPop, self).__init__()
        self.type = type

    def execute(self, thread):
        thread.state.stack.pop(self.type)
        thread.state.pc += 1


class BTZPrint(BTZInst):
    def __init__(self, type):
        super(BTZPrint, self).__init__()
        self.type = type

    def execute(self, thread):
        val = thread.state.stack.peek(self.type)
        if thread.runtime.debug:
            print '[%d]'%thread.id,
        print val
        thread.state.pc += 1
