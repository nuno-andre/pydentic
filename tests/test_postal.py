import logging
import pytest

log = logging.getLogger(__name__)


def test_cn():
    from pydentic.strings.postal_code import CnPostalCode

    code = CnPostalCode('025500')
    assert code == '025500'
    assert code.province == '02'
    assert code.zone == '5'
    assert code.prefecture == '5'
    assert code.area == '00'

    for string in ('02550', '0255001'):
        with pytest.raises(ValueError):
            code = CnPostalCode(string)
