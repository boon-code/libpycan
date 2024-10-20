import re
import cffi

_RX_ATTR = re.compile(r"__attribute__\(.*\)")
_RX_CMT = re.compile(r"/[*].*[*]/")


def _filter(line):
    line = _RX_CMT.sub('', line)
    line = _RX_ATTR.sub('', line)
    if line.startswith('#'):
        if not line.startswith('#define'):
            return ''
    return line


ffibuilder = cffi.FFI()

with open('libpycan.h') as f:
    data = ''.join([_filter(line) for line in f])
    ffibuilder.embedding_api(data)

ffibuilder.set_source("_libpycan", r'''
    #include "libpycan.h"
''')

with open('init.py') as f:
    ffibuilder.embedding_init_code(f.read())

ffibuilder.compile(target="libpycan.*", verbose=True)

