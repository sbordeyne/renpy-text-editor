# py23 compatible
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from ..utils import _fix_all, to_raw, to_str, NoneDict


__all__ = _fix_all(["DAPObject", "DAPBaseMessage"])


class DAPObject(object):

    # BASE METHODS

    @staticmethod
    def determine_root_factory(data):
        pass

    def as_current_kwargs(self):
        return {}

    def to_text(self):
        # print("me=" + str(self) + ", txt=" + str(self.serialize()))  # debug printing
        return json.dumps(self.serialize())

    # SERIALIZATION

    def serialize(self):
        me = {}
        self._serialize(me, [])
        return me

    def _serialize(self, me, override):
        pass

    def serialize_scalar(self, target_dict, target_property, value, hint=None):
        if isinstance(value, dict):
            serialized = {}
            for key in value:
                if isinstance(value[key], DAPObject):
                    serialized[key] = value[key].serialize()
                else:
                    self.serialize_scalar(serialized, key, value[key])
        elif isinstance(value, list) or isinstance(value, tuple):
            serialized = []
            for v in value:
                if isinstance(v, DAPObject):
                    serialized.append(v.serialize())
                else:
                    self.serialize_scalar(serialized, None, v)
        else:
            serialized = value

        if target_property is None:
            # is a list
            target_dict.append(serialized)
        else:
            target_dict[target_property] = serialized

    # DESERIALIZATION
    @staticmethod
    def deserialize(data):
        # print("data=" + str(data))  # debug printing
        factory = DAPObject.determine_root_factory(data)
        return DAPObject.deserialize_as(data, factory)

    @classmethod
    def deserialize_as(cls, data, factory):
        args = []
        kwargs = {}
        factory._deserialize(args, kwargs, [], data, [])
        return factory(*args, **kwargs)

    @classmethod
    def _deserialize(cls, args, kwargs, used_args, me, override):
        pass

    @classmethod
    def deserialize_scalar(cls, value, hint=None):
        if isinstance(value, dict):
            try:
                if hint is not None:
                    return cls.deserialize_as(value, hint)
                return cls.deserialize(value)
            except Exception:
                deserialized = {}
                for key in value:
                    if hint is not None:
                        deserialized[key] = cls.deserialize_as(value[key], hint)
                    else:
                        deserialized[key] = cls.deserialize_scalar(value[key], hint)
        elif isinstance(value, list) or isinstance(value, tuple):
            deserialized = []
            for v in value:
                if hint is not None:
                    deserialized.append(cls.deserialize_as(v, hint))
                else:
                    deserialized.append(cls.deserialize_scalar(v, hint))
        else:
            deserialized = value
        return deserialized


class DAPBaseMessage(DAPObject):
    """
    DAPBaseMessage is base class for all debug adapter protocol messages
    """
    def __init__(self):
        DAPObject.__init__(self)

    @staticmethod
    def recv(socket):
        """
        Retrieves single DAPBaseMessage from socket

        Returns None on failure
        """

        body = DAPBaseMessage.recv_raw(socket)

        if body is not None:
            return DAPObject.deserialize(body)

    @staticmethod
    def recv_raw(socket):
        """
        Retrieves single DAPBaseMessage from socket in raw form (json)

        Returns None on failure
        """

        headers = []

        cread_line = ""

        while True:
            c = socket.recv(1)
            if c is None:
                return None  # failure

            c = to_str(c)
            if c == "":
                # end of stream
                return None
            cread_line += c

            if cread_line.endswith("\r\n"):
                if cread_line == "\r\n":
                    break
                else:
                    headers.append(cread_line)
                    cread_line = ""

        headers = DAPBaseMessage.parse_headers(headers)

        content_size = int(headers["Content-Length"])

        data = ""

        while (len(data) < content_size):
            raw_data = socket.recv(content_size - len(data))
            if raw_data is None:
                return None  # failure
            data += to_str(raw_data)
            if data == "":
                return None

        body = json.loads(data, object_hook=NoneDict)
        # print("RECEIVED: " + str(body))
        return body

    @staticmethod
    def parse_headers(headers):
        """
        Transforms tags into dict
        """

        h = NoneDict({})
        for hl in headers:
            type, value = hl.split(":")
            type = type.strip()
            value = value.strip()
            h[type] = value
        return h

    def send(self, socket):
        """
        Sends this message to client
        """

        data = self.to_text()
        # print("SENT: " + str(data))
        DAPBaseMessage.send_text(socket, data)

    @staticmethod
    def send_text(socket, text):
        """
        Sends the raw text message as DAPBaseMessage
        """

        socket.sendall(to_raw("Content-Length: " + str(len(text)) + "\r\n"))
        socket.sendall(to_raw("\r\n"))
        socket.sendall(to_raw(text))
