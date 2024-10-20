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
    global _bus
    if _bus is not None:
        return lib.PYCAN_RESULT_ALREADY
    _bus = can.Bus()
    return lib.PYCAN_RESULT_OK


def _to_utf8(c_buffer):
    return ffi.string(c_buffer).decode('utf-8')


@ffi.def_extern()
def CanInit(interface, channel, bitrate):
    global _bus
    if _bus is not None:
        return lib.PYCAN_RESULT_ALREADY
    try:
        iface = _to_utf8(interface)
        ch = _to_utf8(channel)
        _bus = can.Bus(
                interface=iface,
                channel=ch,
                bitrate=bitrate,
                single_handle=True
        )
    except:
        return lib.PYCAN_RESULT_FAIL
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanDeinit():
    global _bus
    if _bus is None:
        return lib.PYCAN_RESULT_NOT_INIT
    tmp = _bus
    _bus = None
    try:
        tmp.shutdown()
        return lib.PYCAN_RESULT_OK
    except:
        return lib.PYCAN_RESULT_FAIL


@ffi.def_extern()
def CanRead(buffer, buffer_size, timeout, n_frames_read):
    global _bus
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    if _bus is None:
        return lib.PYCAN_RESULT_NOT_INIT
    count = 0
    t = None
    if timeout > 0.0:
        t = timeout
    try:
        for i in range(buffer_size):
            msg = _bus.recv(timeout=t)
            if msg is None:
                break
            # TODO: map ext, rtr, err bits here
            buffer[i].can_id = msg.arbitration_id
            buffer[i].len = msg.dlc
            buffer[i].flags = 0
            for j in range(msg.dlc):
                buffer[i].data[j] = msg.data[j]
            count += 1
    except can.CanError:
        return lib.PYCAN_RESULT_READ_ERROR
    except:
        return lib.PYCAN_RESULT_FAIL
    if n_frames_read != ffi.NULL:
        n_frames_read[0] = count
    if count < buffer_size:
        return lib.PYCAN_RESULT_INCOMPLETE
    return lib.PYCAN_RESULT_OK


def _to_message(buffer):
    return can.Message(
        # TODO: map ext, rtr, err bits here
        arbitration_id=buffer.can_id,
        is_extended=False,
        dlc=buffer.len,
        data=bytes(buffer.data),
    )


@ffi.def_extern()
def CanWrite(buffer, n_frames):
    global _bus
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    if _bus is None:
        return lib.PYCAN_RESULT_NOT_INIT
    try:
        for i in range(n_frames):
            msg = _to_message(buffer[i])
            while True:
                try:
                    _bus.send(msg)
                    break
                except can.CanError:
                    pass
    except:
        return lib.PYCAN_RESULT_FAIL
    return lib.PYCAN_RESULT_OK


@ffi.def_extern()
def CanTryWrite(buffer, n_frames, timeout, n_frames_written):
    global _bus
    if buffer == ffi.NULL:
        return lib.PYCAN_RESULT_NULL_ARG
    if _bus is None:
        return lib.PYCAN_RESULT_NOT_INIT
    count = 0
    t = None
    if timeout > 0.0:
        t = timeout
    try:
        for i in range(buffer_size):
            msg = can.Message(
                # TODO: map ext, rtr, err bits here
                arbitration_id=buffer[i].can_id,
                is_extended=False,
                dlc=buffer[i].len,
                data=bytes(buffer[i]),
            )
            _bus.send(msg, timeout=t)
            count += 1
    except can.CanError:
        return lib.PYCAN_RESULT_WRITE_ERROR
    except:
        return lib.PYCAN_RESULT_FAIL
    if n_frames_written != ffi.NULL:
        n_frames_written[0] = count
    if count < buffer_size:
        return lib.PYCAN_RESULT_INCOMPLETE
    return lib.PYCAN_RESULT_OK
