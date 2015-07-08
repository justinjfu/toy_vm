TYPE_TO_SIZE = {
    'i': 4,
    'l': 8,
    'f': 4,
    'd': 8
}

TYPE_TO_STRUCT = {
    'i': '>i',
    'l': '>q',
    'f': '>f',
    'd': '>d'
}

TYPE_TO_CAST_PY = {
    'i': int,
    'l': int,
    'f': float,
    'd': float
}

DATA_TYPES = ['i', 'l', 'f', 'd']