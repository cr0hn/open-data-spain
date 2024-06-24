import msgpack


class MessagePackError(Exception):
    pass


def msgpack_dump(obj: dict) -> bytes:
    try:
        return msgpack.packb(obj, use_bin_type=True)
    except Exception as e:
        raise MessagePackError(e)


def msgpack_load(obj: bytes | str) -> dict:
    try:
        return msgpack.unpackb(obj, raw=False)
    except Exception as e:
        raise MessagePackError(e)


__all__ = ("msgpack_dump", "msgpack_load", "MessagePackError")
