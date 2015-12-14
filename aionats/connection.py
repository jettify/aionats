import asyncio
import json
import socket
import sys
import traceback
import warnings

from urllib.parse import urlsplit

from .utils import _ContextManager


__all__ = ['Connection']


class Connection:
    _source_traceback = None

    def __init__(self, uri, name=None, ssl_requred=False, verbose=False,
                 pedantic=False, keepalive=True, loop=None):
        self._uri = uri
        self._name = name
        self._ssl_required = ssl_requred
        self._verbose = verbose
        self._pedantic = pedantic
        self._keepalive = keepalive

        self._reader = None
        self._writer = None

        parsed = urlsplit(uri)
        self._host = parsed.hostname
        self._port = parsed.port
        self._user = parsed.username
        self._password = parsed.password

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

    async def connect(self):
        reader, writer = await asyncio.open_connection(self._host, self._port,
                                                     loop=self._loop)
        self._reader = reader
        self._writer = writer
        transport = self._writer.transport
        raw_sock = transport.get_extra_info('socket', default=None)
        raw_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if self._keepalive:
            raw_sock.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        # TODO: think about adding timeout to the socket

    def _config(self):
        config = {
            'verbose': self._verbose,
            'pedantic': self._pedantic,
            'ssl_requred': self._ssl_required,
            'name': self._name,
        }
        if self._user is not None:
            config['user'] = self._user
            config['pass'] = self._password
        return json.dumps(config)

    def execut(cmd, *args):



    def __del__(self):
        if not self.closed:
            self.close()
            warnings.warn("Unclosed connection {!r}".format(self),
                          ResourceWarning)

            context = {'connection': self,
                       'message': 'Unclosed connection'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return

    def close(self):
        self._reader = None
        self._writer.transport.close()
        self._writer = None
