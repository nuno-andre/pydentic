from typing import Type, TypeVar, NamedTuple, Optional, Pattern, Dict
from os import PathLike
import logging
import re

from ...exceptions import ContentError
from .grammar import Grammar, Rule
from ...core.utils import parse_params, unname_groups

T = TypeVar('T')

log = logging.getLogger(__name__)


def uri_pattern(
    scheme:    str = '[^:/?#]+',
    authority: str = '[^/?#]*',
    path:      str = '[^?#]*',
    query:     str = '[^#]*',
    fragment:  str = '.*',
) -> str:
    '''`URI syntax`__.

    __ https://tools.ietf.org/html/rfc3986#appendix-B
    '''
    pattern = [f'((?P<scheme>{scheme}):)?']
    if authority is not None:
        pattern.append(f'(//(?P<authority>{authority}))?')
    if path is not None:
        pattern.append(f'(?P<path>{path})')
    if query is not None:
        pattern.append(rf'(\?(?P<query>{query}))?')
    if fragment is not None:
        pattern.append(f'(#(?P<fragment>{fragment}))?')
    return '^(?i:{})$'.format(''.join(pattern))


URI = re.compile(uri_pattern())


class ParsedUri(NamedTuple):
    scheme:    Optional[str] = None
    authority: Optional[str] = None
    path:      str = ''
    query:     Optional[str] = None
    fragment:  Optional[str] = None

    @classmethod
    def from_str(cls, string: str, pattern: Pattern = URI) -> 'ParsedUri':
        try:
            match = pattern.match(string).groupdict()
        except AttributeError:
            raise ValueError(string) from None

        if 'scheme' in match:
            match['scheme'] = match['scheme'].lower()

        return cls(**match)

    def __str__(self) -> str:
        # https://tools.ietf.org/html/rfc3986#section-5.3

        # check None to make distinction between undefined components
        # (missing separator) and empty components (separator is present).
        result = []
        if self.scheme is not None:
            result.extend([self.scheme, ':'])
        if self.authority is not None:
            result.extend(['//', self.authority])
        result.append(self.path)
        if self.query is not None:
            result.extend(['?', self.query])
        if self.fragment is not None:
            result.extend(['#', self.fragment])
        return ''.join(result)


class AnyUri(str):
    def __init_subclass__(cls, **kwargs: str):
        cls._pattern = re.compile(uri_pattern(**kwargs))

    def __new__(cls: Type[T], string: str, **kwargs) -> T:
        try:
            parsed = cls._pattern.match(string).groupdict()
        except AttributeError:
            raise ValueError(string) from None

        self = super().__new__(cls, string)

        # set pattern's non-URI named groups as instance attributes
        #   e.g. `nid` and `nss` in AnyUrn
        for field in list(parsed):
            if field not in ParsedUri._fields:
                setattr(self, field, parsed.pop(field))
        if 'scheme' in parsed:
            parsed['scheme'] = parsed['scheme'].lower()
        self.uri = ParsedUri(**parsed)

        return self

    @classmethod
    def __modify_schema__(cls, field_schema) -> None:
        pattern = unname_groups(cls._pattern.pattern)
        field_schema.update(type='string', pattern=pattern)


class SqliteUri(PathLike, AnyUri, scheme='sqlite', authority=''):

    # XXX: fspath protocol not working as SqliteUri subclasses str
    # https://www.python.org/dev/peps/pep-0519/#standard-library-changes
    def __fspath__(self) -> str:
        if not self.uri.path:
            raise OSError(':memory: database')
        return self.uri.path


class GeoUri(
    AnyUri,
    scheme='geo',
    authority=None,
    path=(r'(?P<lat>-?\d{{1,2}}(\.\d+)?)'
          r',(?P<lon>-?\d{{1,3}}(\.\d+)?)'
          r'(,(?P<alt>{NUM}))?'
          r'(;crs=(?-i:(?P<crs>wsg84)))?'
          r'(;u=(?P<unc>{PNUM}))?'
          r'(;(?P<params>.*?))?'
          ).format_map(Grammar),
    fragment=None,
):
    '''`geo URI`__.

    Attributes:
        lat: WGS84 latitude. Decimal degrees.
        lon: WGS84 longitude. Decimal degrees.
        alt: (optional) WGS84 altitude. Decimal meters above the local
            reference ellipsoid.
        unc: (optional) uncertainty in meters.
        crs: `wgs84` is the default value and the only reference system
            supported.

    __ https://tools.ietf.org/html/rfc5870
    '''

    def __init__(self, string: str) -> None:
        self.crs = self.crs or 'wsg84'
        if self.params:
            self.params = parse_params(self.params)
            if 'crs' in self.params or 'u' in self.params:
                err = ("'crs' and 'u' can only appear once, in that order, "
                       "and before other parameters")
                raise ContentError(string, err)

    def __geo_interface__(self) -> Dict:
        if self.alt is None:
            coordinates = (self.lon, self.lat)
        else:
            coordinates = (self.lon, self.lat, self.alt)
        return dict(type='Point', coordinates=coordinates)
