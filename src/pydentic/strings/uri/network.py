from .base import AnyUri, Rule


class StunUri(
    AnyUri,
    scheme='stuns?',
    authority=None,
    path=Rule.HOSTPORT,
    query=None,
    fragment=None,
):
    '''Session Traversal Utilities for NAT (STUN).

    Attributes:
        host: STUN server.
        port:
        secure:
    '''
    @property
    def secure(self) -> bool:
        return self.uri.scheme == 'stuns'

    def __init__(self, string):
        if not self.port:
            self.port = '5349' if self.secure else '3478'

    def __str__(self) -> str:
        return f'{self.uri.scheme}:{self.host}:{self.port}'


class TurnUri(
    AnyUri,
    scheme='turns?',
    authority=None,
    path=Rule.HOSTPORT,
    fragment=None,
):
    '''Traversal Using Relays around NAT (TURN).

    Attributes:
        host:
        port:
        transport:
        secure:
    '''
    @property
    def secure(self) -> bool:
        return self.uri.scheme == 'turns'

    def __init__(self, string):
        if self.query:
            self.query = {k.lower(): v for k, v in self.query.items()}
            if list(self.keys()) != ['transport']:
                # TODO: set in subclass params
                raise ValueError("no param other than 'transport' is allowed")
            self.transport = self.query['transport']


# TODO
class SocksUri(
    AnyUri,
    scheme='socks(4|4a|5|5h)',
):
    '''SOCKS protocol.

    Atributes:
        remote_dns_resolution: if `True` (socks4a, socks5h) the hostname
            is resolved by the SOCKS server. Otherwise (socks4, socks5),
            it's locally resolved.
    '''
    @property
    def remote_dns_resolution(self):
        return self.scheme in {'socks4a', 'socks5h'}


# TODO: raise ValueError if fragment in uri
class WebSocketUri(
    AnyUri,
    scheme='wss?',
    authority=Rule.HOSTPORT,
    fragment=None,
):
    '''`WebSocket Protocol`__

    Attributes:
        host:
        port:
        secure:
        resource: path and query (if any). Fragment is not allowed.

    __ https://tools.ietf.org/html/rfc6455
    '''
    def __init__(self, string):
        if self.port is None:
            self.port = '443' if self.secure else '80'

    @property
    def secure(self) -> bool:
        return self.uri.scheme == 'wss'

    @property
    def resource(self) -> str:
        result = self.uri.path or "/"
        if self.uri.query:
            result += '?' + self.uri.query
        return result

    def __str__(self) -> str:
        return f'{self.uri.scheme}://{self.host}:{self.port}{self.resource}'


__all__ = ['StunUri', 'TurnUri', 'WebSocketUri']
