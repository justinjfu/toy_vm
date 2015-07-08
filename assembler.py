import re
from constants import TYPE_TO_CAST_PY
from ops import *
from operator import add, sub, mul, div

PUSH_RE = re.compile(r'push_[ilfd]')
ADD_RE = re.compile(r'add_[ilfd]')
SUB_RE = re.compile(r'sub_[ilfd]')
MUL_RE = re.compile(r'mul_[ilfd]')
DIV_RE = re.compile(r'div_[ilfd]')
POP_RE = re.compile(r'pop_[ilfd]')
PRINT_RE = re.compile(r'print_[ilfd]')

SPAWN_RE = re.compile(r'spawn_thread')
EXIT_RE = re.compile(r'exit')


def parse_file(fname):
    program = []
    with open(fname) as f:
        for line in f:
            inst = to_inst(line)
            if inst:
                program.append(inst)
    return program

def get_unary_arg(type1, tokens):
    arg1 = tokens[1]
    return TYPE_TO_CAST_PY[type1](arg1)

def get_binary_arg(type1, type2, tokens):
    arg1 = tokens[1]
    arg2 = tokens[2]
    return TYPE_TO_CAST_PY[type1](arg1), TYPE_TO_CAST_PY[type2](arg2)

def to_inst(line):
    line = line.strip()
    if line.startswith('#'): #Comment
        return None
    tokens = re.split('\s+', line)
    op = tokens[0]
    if op == '':
        return None
    elif PUSH_RE.match(op):
        type = op[-1]
        return BTZPush(type, get_unary_arg(type, tokens))
    elif POP_RE.match(op):
        type = op[-1]
        return BTZPop(type)
    elif PRINT_RE.match(op):
        type = op[-1]
        return BTZPrint(type)
    elif ADD_RE.match(op):
        type = op[-1]
        return BTZBinaryOp(type, add)
    elif SUB_RE.match(op):
        type = op[-1]
        return BTZBinaryOp(type, sub)
    elif MUL_RE.match(op):
        type = op[-1]
        return BTZBinaryOp(type, mul)
    elif DIV_RE.match(op):
        type = op[-1]
        return BTZBinaryOp(type, div)
    elif SPAWN_RE.match(op):
        arg1, arg2 = get_binary_arg('i', 'i', tokens)
        return BTZSpawnThread(arg1, arg2)
    elif EXIT_RE.match(op):
        return BTZExit()
    else:
        raise ValueError("Unknown op: ", op)
