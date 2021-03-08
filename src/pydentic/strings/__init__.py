from typing import Union, Optional, Callable, TypeVar, Type, Iterator, Tuple
from types import ModuleType, new_class
from importlib import import_module
from pkgutil import iter_modules
from functools import partial
from pathlib import Path
import sys
import re

import stdnum

from ..exceptions import reraise
# from .uri import AnyUrn

T = TypeVar('T')

DESCR = re.compile(r'^(.*?)\s*?\((.*?)\)')


class Stdnum(str):

    def __init_subclass__(cls, module: Union[str, ModuleType]):
        if isinstance(module, str):
            module = import_module(f'stdnum.{module}')
        cls.__doc__   = module.__doc__.strip().splitlines()[0].rstrip('.')
        cls._validate = lambda v: getattr(module, 'validate')(v)
        cls._format   = lambda v: getattr(module, 'format')(v)
        # if cls.__name__ in {'Issn', 'Isbn', 'Isan'}:
        #     cls.urn = property(lambda s: str(AnyUrn(nid=cls.__name__.lower(),
        #                                             nss=module.compact(s))))

    @classmethod
    def __modify_schema__(cls, field_schema):
        try:
            title, description = DESCR.match(cls.__doc__).groups()
        except AttributeError:
            title, description = cls.__name__, cls.__doc__
        field_schema.update(title=title, description=description)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        yield cls.validate
        yield cls.format

    @classmethod
    def validate(cls, v: str) -> str:
        try:
            return cls._validate(v)
        except Exception as e:
            reraise(e, v)

    @classmethod
    def format(cls: Type[T], v: str) -> T:
        try:
            return cls(cls._format(v))
        except AttributeError:
            return cls(v)
        except Exception as e:
            reraise(e, v)


TERM = ('account', 'catastral', 'code', 'id', 'fiscale',
        'kimlik', 'note', 'numero', 'nummer')

# capitalize the second term in compund words
capitalize = partial(re.compile('({})$'.format('|'.join(TERM))).sub,
                     lambda m: m.group(0).capitalize())


# def traverse_modules(package: ModuleType) -> Tuple[Path, str, Optional[str]]:
#     pkgdir, = map(Path, package.__path__)
#     for _, mod, ispkg in iter_modules([pkgdir]):
#         if ispkg:
#             for _, modsub, _ in iter_modules([pkgdir / mod]):
#                 yield pkgdir, modsub, mod
#         else:
#             yield pkgdir, mod, None

# for path, mod, subpkg in traverse_modules(stdnum):
#     if mod in ():
#         continue


# TODO: decouple with traverse_modules
pkgdir, = stdnum.__path__
for _, mod, ispkg in iter_modules([pkgdir]):
    if ispkg:
        subpkgdir = Path(pkgdir, mod)
        module = ModuleType(f'{__name__}.{mod}')
        module.__path__ = [str(subpkgdir / mod)]
        for _, modsub, _ in iter_modules([subpkgdir]):
            name = capitalize(modsub.capitalize())
            cls = new_class(name, (Stdnum,), {'module': f'{mod}.{modsub}'})
            setattr(module, name, cls)
        globals().update({mod: module})
        sys.modules[f'{__name__}.{mod}'] = module

    elif not mod.startswith('mod_') and mod not in (
            # iso9362 deprecated in favor of bic
            'exceptions', 'numdb', 'util', 'iso9362',
            # algorithms
            'luhn', 'damn', 'verhoeff'):
        name = mod.capitalize()
        globals()[name] = new_class(name, (Stdnum,), {'module': mod})


del (ispkg, iter_modules, mod, modsub, module, ModuleType, partial, Path, re,
     stdnum, Stdnum, subpkgdir, capitalize, cls, name, pkgdir, TERM, new_class)
