from typing import NamedTuple, Optional, Dict
from enum import Enum
import re

from ..core.utils import parse_params

# https://tools.ietf.org/html/rfc2045#section-5.1
# https://tools.ietf.org/html/rfc7231#section-3.1.1.1


class MediaTypes(str, Enum):
    application = 'application'
    audio       = 'audio'
    chemical    = 'chemical'
    example     = 'example'
    font        = 'font'
    image       = 'image'
    message     = 'message'
    model       = 'model'
    multipart   = 'multipart'
    text        = 'text'
    video       = 'video'


# rfc3025, rfc6839
class MediaSuffixes(str, Enum):
    ber         = 'ber'
    cbor        = 'cbor'
    cbor_seq    = 'cbor-seq'
    der         = 'der'
    fastinfoset = 'fastinfoset'
    gzip        = 'gzip'
    json        = 'json'
    json_seq    = 'json-seq'
    jwt         = 'jwt'
    sqlite3     = 'sqlite3'
    tlv         = 'tlv'  # https://en.wikipedia.org/wiki/Type-length-value
    xml         = 'xml'
    wbxml       = 'wbxml'
    zip         = 'zip'


def mime_pattern(type: Optional[str] = None) -> str:
    TOKEN = r'[A-Z0-9-.]+'

    if not type:
        types = '|'.join(m.value for m in MediaTypes)
        type  = f'{types}|x-{TOKEN}'
    suffixes = '|'.join(m.value for m in MediaSuffixes)
    pattern  = (f'(?P<type>{type})/'
                f'(?P<subtype>{TOKEN})'
                fr'(\+(?P<suffix>{suffixes}))?')
    return f'(?i:{pattern})'


def content_type_pattern(type: Optional[str] = None) -> str:
    OWS    = r'[ \t]*'
    TOKEN  = r'[A-Z0-9!#$%&\'*+.^_`|~-]+'
    QUOTED = r'\"(?:[^\"\\\\]|\\.)*\"'
    PARAM  = f';{OWS}{TOKEN}=({TOKEN}|{QUOTED})'

    return f'{mime_pattern(type)}(?P<params>({PARAM})*)'


MIME = re.compile(mime_pattern())

CTYPE = re.compile(content_type_pattern(), re.I)


class MediaType(NamedTuple):
    type:    str
    subtype: str
    suffix:  Optional[str]

    def __str__(self) -> str:
        suffix = f'+{self.suffix}' if self.suffix else ''
        return f'{self.type}/{self.subtype}{suffix}'

    @classmethod
    def from_str(cls, string: str) -> 'MediaType':
        try:
            return cls(**MIME.match(string).groupdict())
        except AttributeError:
            raise ValueError(string)


class ContentType(NamedTuple):
    type:    str
    subtype: str
    suffix:  Optional[str]
    params:  Optional[Dict[str, str]]

    def __str__(self) -> str:
        suffix = f'+{self.suffix}' if self.suffix else ''
        m_type = f'{self.type}/{self.subtype}{suffix}'
        params = [f'{k}={v}' for k, v in (self.params or {}).items()]
        return ';'.join((m_type, *params))

    @property
    def media_type(self) -> MediaType:
        return MediaType(type=self.type, subtype=self.subtype, suffix=self.suffix)

    @classmethod
    def from_str(cls, string: str) -> 'ContentType':
        try:
            ctype = CTYPE.match(string).groupdict()
        except AttributeError:
            raise ValueError(string)

        return cls(type=ctype['type'].lower(),
                   subtype=ctype['subtype'].lower(),
                   suffix=ctype['suffix'].lower() if ctype['suffix'] else None,
                   params=parse_params(ctype['params']))
