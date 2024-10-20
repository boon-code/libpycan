from _libpycan import ffi, lib
import can


_bus = None


@ffi.def_extern()
def GetVersion(version):
    if version == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    version[0].major = 0
    version[0].minor = 1
    version[0].patch = 2
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanInitDefault():
    if _bus is not None:
        return lib.PYCAN_RESULT_ALREADY
    _bus = can.Bus()
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanInit(interface, channel, bitrate):
    if _bus is not None:
        return lib.PYCAN_RESULT_ALREADY
    iface = interface.decode('utf-8')
    ch = channel.decode('utf-8')
    _bus = can.Bus(interface=interface, channel=channel, bitrate=bitrate, single_handle=True)
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanDeinit():
    pass


@ffi.def_extern()
def CanRead(buffer, buffer_size, timeout, n_frames_read):
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    return lib.PYCAN_RESULT_NO_FRAME


@ffi.def_extern()
def CanWrite(buffer, n_frames):
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanTryWrite(buffer, n_frames, timeout, n_frames_written):
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    if n_frames_written == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    return lib.PYCAN_RESULT_INCOMPLETE
