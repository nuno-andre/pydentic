from urllib.request import urlopen
from typing import Optional, Iterator, Tuple, List
from pathlib import Path
import logging
import sqlite3

log = logging.getLogger(__name__)

DATADIR = Path(__file__).parents[1].joinpath('data')
DATADIR.mkdir(exist_ok=True)


class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DATADIR / 'db.sqlite')

    def create_tables(self) -> None:
        log.debug('Creating %s tables...', self.__class__.__name__)
        self.conn.executescript(self._drop_tables)
        self.conn.executescript(self._create_tables)

    def get_source(
        self,
        url:      str,
        encoding: Optional[str] = None,
    ) -> Iterator[str]:

        with urlopen(url) as resp:
            ctype = resp.headers.get_content_type()
            if ctype == 'text/plain':
                if encoding is None:
                    encoding = resp.headers.get_content_charset()
                data = resp.read().decode(encoding or 'utf-8')
                return iter(data.splitlines())
            else:
                return resp.read()

    def populate(self) -> None:
        log.debug('Populating %s tables...', self.__class__.__name__)
        recs = self.parse_source()
        self.conn.executemany(self._insert_item, recs)
        self.conn.commit()


ETLD_URL = 'https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat'


class Etld(Db):
    _create_tables = '''\
        create table etld (
            id         integer primary key autoincrement,
            tld        text not null collate nocase,
            etld       text not null collate nocase,
            registrar  text
        );
        create unique index etld_un on etld (
            tld, etld
        );
    '''

    _drop_tables = 'drop table if exists etld;'

    _insert_item = 'insert into etld (tld, etld, registrar) values (?, ?, ?);'

    def parse_source(self) -> List[Tuple[str, str, str]]:
        recs = list()
        data = self.get_source(ETLD_URL)

        for line in data:
            if '===BEGIN ICANN DOMAINS===' in line:
                break

        while True:
            try:
                line = next(data)
            except StopIteration:
                break

            if not line.strip():
                continue

            registrar = line.lstrip('/ ')

            for line in data:
                if not line.strip():
                    break
                if line.startswith('//'):
                    continue
                tld = line.split('.')[-1]
                recs.append((tld, line, registrar))

        return sorted(recs)
