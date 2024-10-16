import cffi

ffibuilder = cffi.FFI()

with open('libpycan.h') as f:
    data = ''.join([line for line in f if not line.startswith('#')])
    ffibuilder.embedding_api(data)

ffibuilder.set_source("_libpycan", r'''
    #include "libpycan.h"
''')

with open('init.py') as f:
	ffibuilder.embedding_init_code(f.read())

ffibuilder.compile(target="libpycan.*", verbose=True)

