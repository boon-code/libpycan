import re
import cffi

_RX_ATTR = re.compile(r"__attribute__\(.*\)")
_RX_CMT = re.compile(r"/[*].*[*]/")

_REPL_CAN_FRAME = """
	canid_t can_id;  /* 32 bit CAN_ID + EFF/RTR/ERR flags */
	uint8_t    len;     /* frame payload length in byte */
	uint8_t    flags;   /* additional flags for CAN FD */
	uint8_t    data[CANFD_MAX_DLEN];
        ...;
"""


def _filter(line):
    line = _RX_CMT.sub('', line)
    line = _RX_ATTR.sub('', line)
    if line.startswith('#'):
        if not line.startswith('#define'):
            return ''
    return line


def _find_end(data, i):
    level = 1
    for c in data[i:]:
        if c == '{':
            level += 1
        elif c == '}':
            level -= 1
        if level == 0:
            return i
        i += 1
    raise RuntimeError("Missing end of struct")


def _replace_struct(name, data, repl):
    text = "struct " + name + " {"
    i = data.find(text)
    if i < 0:
        raise RuntimeError(f"Struct {name} not found")
    i += len(text)
    pre = data[0:i]
    end = _find_end(data, i)
    assert end >= i, "Index sanity check"
    post = data[end:]
    return pre + '\n' + repl + '\n' + post


ffibuilder = cffi.FFI()

with open('libpycan.h') as f:
    data = ''.join([_filter(line) for line in f])
    data = _replace_struct('canfd_frame', data, _REPL_CAN_FRAME)
    with open('_libpycan.python.h', 'w') as out:
        out.write(data)
    ffibuilder.embedding_api(data)

ffibuilder.set_source("_libpycan", r'''
    #include "libpycan.h"
''')

with open('init.py') as f:
    ffibuilder.embedding_init_code(f.read())

ffibuilder.compile(target="libpycan.*", verbose=True)

