from typing import Optional, NoReturn

from stdnum.exceptions import (
    InvalidChecksum,
    InvalidFormat,
    InvalidComponent,
    InvalidLength as _InvalidLength,
    ValidationError,
)


class PydenticError(ValueError):
    '''Base validation error.
    '''
    def __init__(self, value: str, error: Optional[str] = None):
        if error:
            self.error = error
        super().__init__(value)


class FormatError(PydenticError):
    code = 'format'


class InvalidLength(PydenticError):
    code = 'length'


class ContentError(PydenticError):
    code = 'content'


class ChecksumError(ContentError):
    code = 'checksum'


EXCMAPPING = {
    InvalidChecksum:  ChecksumError,
    InvalidFormat:    FormatError,
    InvalidComponent: ContentError,
    _InvalidLength:   InvalidLength,
    ValidationError:  PydenticError,
    ValueError:       PydenticError,
    TypeError:        PydenticError,
}


def reraise(e: Exception, v: str) -> NoReturn:
    try:
        exc = EXCMAPPING[type(e)]
    except KeyError:
        raise e

    try:
        error = e.__context__.args[0]
    except AttributeError:
        error = None

    raise exc(value=v, error=error)
