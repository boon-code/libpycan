from _libpycan import ffi, lib
import can
from pathlib import Path


_bus = None


def _to_utf8(c_buffer):
    return ffi.string(c_buffer).decode('utf-8')


def _to_message(buffer):
    is_ext = ((buffer.can_id & lib.CAN_EFF_FLAG) != 0)
    is_rtr = ((buffer.can_id & lib.CAN_RTR_FLAG) != 0)
    is_err = ((buffer.can_id & lib.CAN_ERR_FLAG) != 0)
    data = buffer.data[0:buffer.len]
    if is_rtr:
        data = bytes()
    can_id = buffer.can_id & lib.CAN_EFF_MASK
    if not is_ext:
        can_id = buffer.can_id & lib.CAN_SFF_MASK
    if is_err:
        can_id = buffer.can_id & lib.CAN_ERR_MASK
    return can.Message(
        arbitration_id=can_id,
        is_extended_id=is_ext,
        is_remote_frame=is_rtr,
        is_error_frame=is_err,
        dlc=buffer.len,
        data=data,
    )


def _set_c_frame(msg, buffer):
    flags = 0
    if msg.is_extended_id:
        flags |= lib.CAN_EFF_FLAG
    if msg.is_remote_frame:
        flags |= lib.CAN_RTR_FLAG
    if msg.is_error_frame:
        flags |= lib.CAN_ERR_FLAG
    can_id = msg.arbitration_id & lib.CAN_EFF_MASK
    assert can_id == msg.arbitration_id, "identity"
    if not msg.is_extended_id:
        can_id = msg.arbitration_id & lib.CAN_SFF_MASK
    buffer.can_id = can_id | flags
    buffer.len = msg.dlc
    buffer.flags = 0
    if not msg.is_remote_frame:
        for i in range(msg.dlc):
            buffer.data[i] = msg.data[i]


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
    try:
        cfg_path = Path('can.ini')
        if cfg_path.is_file():
            can.rc = can.util.load_config(path=cfg_path)
        _bus = can.Bus(single_handle=True)
    except:
        return lib.PYCAN_RESULT_FAIL
    return lib.PYCAN_RESULT_OK


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
            _set_c_frame(msg, buffer[i])
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
        for i in range(n_frames):
            msg = _to_message(buffer[i])
            _bus.send(msg, timeout=t)
            count += 1
    except can.CanError:
        return lib.PYCAN_RESULT_WRITE_ERROR
    except:
        return lib.PYCAN_RESULT_FAIL
    if n_frames_written != ffi.NULL:
        n_frames_written[0] = count
    if count < n_frames:
        return lib.PYCAN_RESULT_INCOMPLETE
    return lib.PYCAN_RESULT_OK
