"""
Implementation of VM state
"""

from stack import VMStack

MASTER_THREAD_ID = 0


class VMRuntime(object):
    def __init__(self, program):
        # program = list of instructions
        self.program = program
        self.memory = None  # TODO
        self.threads = {}
        self.done = False
        self.debug = False

        self.threads_to_kill = []
        self.threads_to_add = []
        self.highest_thread_id = MASTER_THREAD_ID

    def get_inst(self, pc):
        return self.program[pc]

    def run(self):
        self.timestep = 0
        while not self.done:
            self.step()
            self.timestep += 1

    def step(self):
        for thread in self.threads:
            self.threads[thread].step()

        for thread in self.threads_to_kill:
            if self.debug:
                print '[Runtime:%d] Killing thread %d' % (self.timestep, thread)
            del self.threads[thread]
        self.threads_to_kill = []

        for thread in self.threads_to_add:
            if self.debug:
                print '[Runtime:%d] Spawning thread %d' % (self.timestep, thread.id)
            self.threads[thread.id] = thread
        self.threads_to_add = []

        if len(self.threads) == 0:
            if self.debug:
                print '[Runtime:%d] Done' % self.timestep
            self.done = True

    def spawn_master(self):
        master = VMThread(self, 0, MASTER_THREAD_ID)
        self.threads[0] = master

    def command_kill_thread(self, id):
        self.threads_to_kill.append(id)

    def command_spawn_thread(self, new_stack, pc):
        self.highest_thread_id += 1
        new_thread = VMThread(self, pc, self.highest_thread_id)
        new_thread.state.stack = new_stack
        self.threads_to_add.append(new_thread)


class VMThreadState(object):
    def __init__(self):
        self.pc = 0
        self.stack = VMStack()
        self.alive = True

    def __repr__(self):
        return '{pc=%d, alive=%s, stack=%s}' % (self.pc, self.alive, self.stack)


class VMThread(object):
    def __init__(self, runtime, init_pc, id):
        self.runtime = runtime
        self.state = VMThreadState()
        self.state.pc = init_pc
        self.id = id

    def step(self):
        inst = self.runtime.get_inst(self.state.pc)
        inst.execute(self)

    def __repr__(self):
        return '%r ==> %r' % (self.state, self.runtime.get_inst(self.state.pc))
