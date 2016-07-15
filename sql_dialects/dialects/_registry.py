import pkg_resources
import warnings

from sql_dialects.exceptions import NoDefaultDialect
from sql_dialects.dialects._base import SQLDialect

__author__ = 'Aaron Hosford'


# TODO: Support alternate names for dialects.

class DialectRegistry:

    def __init__(self):
        self._dialects_by_name = {}
        self._dialects = set()
        self._default_dialect = None

    @property
    def default(self):
        return self._default_dialect

    @default.setter
    def default(self, dialect):
        if isinstance(dialect, str):
            dialect = self[dialect]
        self.add(dialect, set_default=True)

    @default.deleter
    def default(self):
        self._default_dialect = None

    def load(self):
        for entry_point in pkg_resources.iter_entry_points(group='sql_dialects'):
            try:
                self.add(entry_point.load())
            except Exception as exc:
                warnings.warn(str(exc))

    def add(self, dialect, set_default=False):
        assert isinstance(dialect, SQLDialect)

        lower_name = dialect.name.lower()
        assert lower_name != 'default', "Dialect cannot be named 'default'."

        if lower_name in self._dialects_by_name:
            self._dialects.discard(self._dialects_by_name[lower_name])

        self._dialects_by_name[lower_name] = dialect
        self._dialects.add(dialect)

        if set_default:
            self._default_dialect = dialect

    def remove(self, dialect):
        if isinstance(dialect, str):
            dialect = self[dialect]

        del self._dialects_by_name[dialect.name.lower()]
        self._dialects.remove(dialect)

        if self._default_dialect == dialect:
            self._default_dialect = None

    def discard(self, dialect):
        if dialect in self:
            self.remove(dialect)

    def get(self, item, default=None):
        if item in self:
            return self[item]
        else:
            return default

    def __getitem__(self, item):
        if item is None or (isinstance(item, str) and item.lower() == 'default'):
            if self._default_dialect is None:
                raise NoDefaultDialect(item)
            return self._default_dialect
        elif isinstance(item, SQLDialect):
            if item not in self._dialects:
                raise KeyError(item)
            return item
        else:
            assert item and isinstance(item, str)
            return self._dialects_by_name[item.lower()]

    def __iter__(self):
        return iter(self._dialects)

    def __len__(self):
        return len(self._dialects)

    def __contains__(self, item):
        if item is None or (isinstance(item, str) and item.lower() == 'default'):
            return self._default_dialect is not None
        elif isinstance(item, SQLDialect):
            return item in self._dialects
        else:
            assert item and isinstance(item, str)
            return item.lower() in self._dialects_by_name
