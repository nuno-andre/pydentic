from enum import Enum
import re


class Grammar(str, Enum):
    ALPHANUM    = '0-9a-zA-Z'
    HEXDIG      = '0-9a-fA-F'
    PNUM        = r'\d+(\.\d+)?'
    NUM         = f'-?{PNUM}'
    MARK        = re.compile("-_.!~*'/()")  # https://tools.ietf.org/html/rfc5870#section-3.3
    PCT_ENCODED = f'%[{HEXDIG}][{HEXDIG}]'


class Rule(str, Enum):
    HOSTPORT     = r'(?P<host>[^/?#:]+)(?:\:(?P<port>\d+))?'
    # FIXME: remove lookbehinds
    #   https://json-schema.org/understanding-json-schema/reference/regular_expressions.html
    USERHOSTPORT = (r'(?:(?P<user>[^@]*)@)'
                    r'\[?(?P<host>(?<=\[).+(?=\])|([^:]+))\]?'
                    r'(?:\:(?P<port>\d+))?')
