import pytest
import logging

from pydentic.exceptions import ContentError

log = logging.getLogger(__name__)


def test_geo():
    from pydentic.strings.uri import GeoUri

    geo = GeoUri('geo:48.2010,16.3695,183')
    assert (geo.lat, geo.lon, geo.alt) == ('48.2010', '16.3695', '183')
    assert geo.unc is None
    assert geo.crs == 'wsg84'

    geo = GeoUri('geo:48.2010,16.3695,183;crs=wsg84;u=12;param=value')

    with pytest.raises(ContentError):
        GeoUri('geo:48,16;crs=wsg84;u=1;crs=wsg84;u=1')


def test_stun():
    from pydentic.strings.uri import StunUri

    assert StunUri('stun:example.com:8000') == 'stun:example.com:8000'
    assert StunUri('stun:example.com').port == '3478'
    assert StunUri('stuns:example.com').port == '5349'
    assert StunUri('stun:example.com').secure is False
    assert StunUri('stuns:example.com').secure is True


def test_websocket():
    from pydentic.strings.uri import WebSocketUri

    # TODO:
    # with pytest.raises(ValueError):
    #     # fragment not allowed
    #     WebSocketUri('ws://host:80/path?query#fragment')

    ws = WebSocketUri('ws://host/path?query')
    assert ws.host == 'host'
    assert ws.port == '80'
    assert ws.resource == '/path?query'

    assert WebSocketUri('ws://host/path?query').secure is False
    assert WebSocketUri('wss://host/path?query').secure is True
