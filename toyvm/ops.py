"""
Implementations of instructions
"""

class BTZInst(object):
    def __init__(self, line_num, code_num):
        self.line_num = line_num
        self.code_num = code_num

    def execute(self, thread, runtime):
        raise NotImplementedError()

    def __repr__(self):
        return '%s@%d' % (self.__class__.__name__, self.line_num)

    def to_c(self, labeler):
        raise NotImplementedError()


class BTZNop(BTZInst):
    def execute(self, thread, runtime):
        thread.state.pc += 1


class BTZExit(BTZInst):
    def execute(self, thread, runtime):
        if thread.state.alive:
            thread.state.alive = False
            runtime.command_kill_thread(thread.id)
        else:
            raise ValueError('Thread already dead: '+thread.id)

    def to_c(self, labeler):
        return 'return 0'

class BTZSpawnThread(BTZInst):
    def __init__(self, line, code, pc_offset, top_bytes):
        super(BTZSpawnThread, self).__init__(line, code)
        self.top_bytes = top_bytes
        self.pc_offset = pc_offset
        assert pc_offset != 0  # Offset=0 creates an infinite loop

    def execute(self, thread, runtime):
        new_stack = thread.state.stack.clone(top_bytes=self.top_bytes)
        runtime.command_spawn_thread(new_stack, thread.state.pc+self.pc_offset)
        thread.state.pc += 1

    def to_c(self, labeler):
        raise NotImplementedError('Threading not implemented in compiler')


class BTZBinaryOp(BTZInst):
    def __init__(self, line, code, type, op):
        super(BTZBinaryOp, self).__init__(line, code)
        self.op = op
        self.type = type

    def execute(self, thread, runtime):
        b = thread.state.stack.pop(self.type)
        a = thread.state.stack.pop(self.type)
        thread.state.stack.push(self.type, self.op(a,b))
        thread.state.pc += 1

    def __repr__(self):
        return '%s_%s' % (self.op.__name__, self.type)

    def to_c(self, labeler):
        return '%s(%s)' % (self.op.__name__, self.type)


class BTZPush(BTZInst):
    def __init__(self, line, code, type, value):
        super(BTZPush, self).__init__(line, code)
        self.value = value
        self.type = type

    def execute(self, thread, runtime):
        thread.state.stack.push(self.type, self.value)
        thread.state.pc += 1

    def __repr__(self):
        return 'push_%s:%s' % (self.type, self.value)

    def to_c(self, labeler):
        return 'push(%s,%s)' % (self.type, self.value)


class BTZPop(BTZInst):
    def __init__(self, line, code, type):
        super(BTZPop, self).__init__(line, code)
        self.type = type

    def execute(self, thread, runtime):
        thread.state.stack.pop(self.type)
        thread.state.pc += 1

    def to_c(self, labeler):
        return 'pop(%s)' % (self.type)


class BTZClone(BTZInst):
    def __init__(self, line, code, type):
        super(BTZClone, self).__init__(line, code)
        self.type = type

    def execute(self, thread, runtime):
        val = thread.state.stack.peek(self.type)
        thread.state.stack.push(self.type, val)
        thread.state.pc += 1

    def to_c(self, labeler):
        return 'clone(%s)' % (self.type)


class BTZPrint(BTZInst):
    def __init__(self, line, code, type):
        super(BTZPrint, self).__init__(line, code)
        self.type = type

    def execute(self, thread, runtime):
        val = thread.state.stack.peek(self.type)
        if runtime.debug:
            print '[%d]'%thread.id,
        print val
        thread.state.pc += 1

    def to_c(self, labeler):
        return 'print(%s)' % (self.type)


class BTZBeq(BTZInst):
    def __init__(self, line, code, pc_offset):
        super(BTZBeq, self).__init__(line, code)
        self.pc_offset = pc_offset

    def execute(self, thread, runtime):
        val = thread.state.stack.pop('i')
        if val:
            thread.state.pc += self.pc_offset
        else:
            thread.state.pc += 1

    def to_c(self, labeler):
        label = labeler.get_label(self.code_num-1+self.pc_offset)
        return 'b(%s)' % label


class BTZJumpOffset(BTZInst):
    def __init__(self, line, code, pc_offset):
        super(BTZJumpOffset, self).__init__(line, code)
        self.pc_offset = pc_offset

    def execute(self, thread, runtime):
        thread.state.pc += self.pc_offset

    def to_c(self, labeler):
        label = labeler.get_label(self.code_num-1+self.pc_offset)
        return 'j(%s)' % label


class BTZJumpStack(BTZInst):
    def __init__(self, line, code):
        super(BTZJumpStack, self).__init__(line, code)

    def execute(self, thread, runtime):
        val = thread.state.stack.pop('i')
        thread.state.pc = val


class BTZStoreMem(BTZInst):
    def __init__(self, line, code, type):
        super(BTZStoreMem, self).__init__(line, code)
        self.type = type

    def execute(self, thread, runtime):
        idx = thread.state.stack.pop('i')
        val = thread.state.stack.pop(self.type)
        runtime.command_storemem(self.type, idx, val)
        thread.state.pc += 1

    def to_c(self, labeler):
        return 'memstore(%s)' % (self.type)


class BTZReadMem(BTZInst):
    def __init__(self, line, code, type):
        super(BTZReadMem, self).__init__(line, code)
        self.type = type

    def execute(self, thread, runtime):
        idx = thread.state.stack.pop('i')
        val = runtime.memory.read(self.type, idx)
        thread.state.stack.push(self.type, val)
        thread.state.pc += 1

    def to_c(self, labeler):
        return 'memread(%s)' % (self.type)
