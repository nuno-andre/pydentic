"""
String munging utils.
"""
from typing import Optional, List, Dict
from functools import partial
import re


#: Removes capture groups' name (for JSON Schema patterns)
unname_groups = partial(re.compile(r'\(\?P<\w+>').sub, '(')


def segment(string: str, *sizes: int, start: int = 0) -> List[str]:
    '''Splits the string into the indicated number and size of pieces.

    >>> segment('0123456789ABCDEF', 3, 4, 5, 4)
    ['012', '3456', '789AB', 'CDEF']
    '''
    from itertools import accumulate, tee

    a, b = tee(accumulate((start, *sizes)))
    next(b, None)
    return [string[slice(*ab)] for ab in zip(a, b)]


def parse_params(
    string:     Optional[str],
    sep:        str = ';',
    whitespace: bool = False,
) -> Optional[Dict[str, str]]:
    '''Parses a string of parameters and values, and normalizes
    parameters to lowercase.

    Args:
        whitespace: strips whitespace between params.

    >>> parse_params('a=b;C=D')
    {'a': 'b', 'c': 'D'}
    '''
    if not string or not string.strip():
        return None

    if whitespace:
        params = filter(None, map(str.strip, string.split(sep)))
        params = (p.split('=') for p in params)
    else:
        params = (p.split('=') for p in string.strip().split(sep))

    return {k.lower(): v for k, v in params}


def slug(text: str, to_identifier: bool = False) -> str:
    import unicodedata

    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf-8').casefold()
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-z_-]', '', text)

    return str(text)


class SnakeCasing:
    '''Formats text strings in snake case.
    '''
    def __init__(self):
        self.prep = re.compile('(.)([A-Z][a-z]+)')
        self.ptrn = re.compile('([a-z0-9])([A-Z])')

    def __call__(self, text):
        text = self.prep.sub(r'\1_\2', text)
        return self.ptrn.sub(r'\1_\2', text).casefold()


to_snake = partial(SnakeCasing())


def to_camel(string: str) -> str:
    first, *rest = string.split('_')
    return ''.join([first, *map(str.capitalize, rest)])


def to_pascal(string: str) -> str:
    return ''.join(map(str.capitalize, string.split('_')))
