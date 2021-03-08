from typing import Type, TypeVar
import re

from .utils import unname_groups

T = TypeVar('T')


class RegExpString(str):
    def __init_subclass__(cls, pattern: str):
        cls._pattern = re.compile(pattern)

    def __new__(cls: Type[T], string: str, **kwargs) -> T:
        try:
            parsed = cls._pattern.match(string).groupdict()
        except AttributeError:
            raise ValueError(string) from None

        self = super().__new__(cls, string)

        # set pattern's named groups as instance attributes
        for field in list(parsed):
            setattr(self, field, parsed.pop(field))

        return self

    @classmethod
    def __modify_schema__(cls, field_schema) -> None:
        pattern = unname_groups(cls._pattern.pattern)
        field_schema.update(type='string', pattern=pattern)


__all__ = ['RegExpString']
