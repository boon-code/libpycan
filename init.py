from _libpycan import ffi
import can

@ffi.def_extern()
def GetVersion(version):
    # TODO: null check
    version[0].major = 0
    version[0].minor = 1
    version[0].patch = 2
    return 0
