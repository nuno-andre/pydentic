import logging

log = logging.getLogger(__name__)


# def test_urn():
#     from pydentic.strings import Isan, Isbn, Issn

#     assert Isbn('978-0-465-02656-2').urn == 'urn:isbn:9780465026562'
#     isan = 'ISAN 0000-0000-3A8D-0000-Z-0000-0000-6'


def test_mac():
    from pydentic.strings import Mac

    for mac in ('00:11:22:dd:ee:ff',  # standard format
                '00-11-22-DD-EE-FF',
                '1b:7749:54fd',       # Cisco format
                '001122:DDEEFF',      # PostgreSQL format
                '001.122.DDE.EFF'):
        log.info(Mac(mac))
