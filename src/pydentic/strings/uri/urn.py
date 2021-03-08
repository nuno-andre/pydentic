from .base import AnyUri


def urn_path(
    nid: str = '[A-Z0-9][A-Z0-9-]{1,31}',
    nss: str = '[^:]*?',  # TODO
):
    '''`URN syntax`__.

    Args:
        nid: Namespace identifier (IANA registered).
        nss: Namespace-specific string.

    __ https://tools.ietf.org/html/rfc2141#section-2
    '''
    return (rf'(?i:(?P<nid>{nid})):'
            rf'(?P<nss>{nss})$')


class AnyUrn(AnyUri, scheme='urn', authority=None, path=urn_path()):

    def __str__(self):
        return f'urn:{self.nid}:{self.nss}'


class IssnUrn(AnyUrn, path=urn_path('issn')):

    def __url__(self):
        return f'https://urn.issn.org/{self}'


# FIXME: this is DOI specific
HANDLEID = r'(?P<prefix>10\.[1-9]\d{3}(\.\d+)?)/(?P<suffix>.*)$'


class HandleUrn(AnyUrn, path=urn_path('hdl', HANDLEID)):
    '''
    Attributes:
        prefix: naming authority
        suffix: unique local name
    '''
    def __url__(self):
        return f'http://hdl.handle.net/{self.prefix}/{self.suffix}'


class DoiUri(AnyUri, scheme='doi', authority=None, path=HANDLEID):

    def __str__(self):
        return f'doi:{self.prefix}/{self.suffix}'

    def __url__(self):
        return f'https://doi.org/{self.prefix}/{self.suffix}'


__all__ = ['AnyUrn', 'IssnUrn', 'HandleUrn', 'DoiUri']

del (urn_path, HANDLEID)
