import logging
import pytest

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def test_import_modules():
    import pydentic
    from pydentic import strings
    from pydentic.strings import ad
    from pydentic.strings.ad import Nrt


def test_reraise():
    from pydentic.exceptions import EXCMAPPING, reraise

    for stdexc, pydexc in EXCMAPPING.items():
        with pytest.raises(pydexc):
            try:
                raise stdexc('error')
            except Exception as e:
                reraise(e, 'value')
