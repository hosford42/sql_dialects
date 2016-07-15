import datetime
import decimal

__author__ = 'Aaron Hosford'


class Nullary:
    """
    Operators/functions that accept zero arguments.
    """

    NOW = 'now'         # Current date/time
    GUID = 'guid'       # Globally unique identifier
    VERSION = 'version' # Database version

    @classmethod
    def iter(cls):
        return iter((cls.NOW, cls.GUID, cls.VERSION))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()


class Unary:
    """
    Operators/functions that accept one argument.
    """

    NOT = 'not'
    NEG = '-'
    UPPER_CASE = 'upper case'
    LOWER_CASE = 'lower case'
    LENGTH = 'length'

    @classmethod
    def iter(cls):
        return iter((cls.NOT, cls.NEG, cls.UPPER_CASE, cls.LOWER_CASE, cls.LENGTH))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()


class Binary:
    """
    Operators/functions that accept two arguments.
    """

    EQ = '=='
    NE = '!='
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='
    AND = 'and'
    OR = 'or'
    ROUND = 'round'
    FORMAT = 'format'

    @classmethod
    def iter(cls):
        return iter((cls.EQ, cls.NE, cls.LT, cls.GT, cls.LE, cls.GE, cls.AND, cls.OR, cls.ROUND,
                     cls.FORMAT))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()


class Ternary:
    """
    Operators/functions that accept three arguments.
    """

    SUBSTRING = 'substring'
    IF_ELSE = 'if/else'

    @classmethod
    def iter(cls):
        return iter((cls.SUBSTRING, cls.IF_ELSE))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()


class Aggregate:
    """
    Operators/functions that accept one aggregate argument.
    """

    SUM = 'sum'
    MAX = 'max'
    MIN = 'min'
    AVG = 'avg'
    COUNT = 'count'
    FIRST = 'first'
    LAST = 'last'

    @classmethod
    def iter(cls):
        return iter((cls.SUM, cls.MAX, cls.MIN, cls.AVG, cls.COUNT, cls.FIRST, cls.LAST))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()


class LiteralTypes:
    NULL = 'null'
    STRING = 'string'
    INTEGER = 'integer'
    DATE = 'date'
    DATE_TIME = 'date/time'
    FLOAT = 'float'

    _map = {
        NULL: type(None),
        STRING: str,
        INTEGER: int,
        DATE: datetime.date,
        DATE_TIME: datetime.datetime,
        FLOAT: (float, decimal.Decimal)
    }

    _reverse_map = {
        type(None): NULL,
        str: STRING,
        int: INTEGER,
        datetime.date: DATE,
        datetime.datetime: DATE_TIME,
        float: FLOAT,
        decimal.Decimal: FLOAT
    }

    @classmethod
    def iter(cls):
        return iter(cls._map)

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls._map

    @classmethod
    def get_python_type(cls, sql_type):
        return cls._map[sql_type]

    @classmethod
    def get_sql_type(cls, python_type):
        return cls._reverse_map[python_type]


class JoinTypes:
    INNER = 'inner'
    LEFT = 'left'
    RIGHT = 'right'
    OUTER = 'outer'

    @classmethod
    def iter(cls):
        return iter((cls.INNER, cls.LEFT, cls.RIGHT, cls.OUTER))

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in cls.iter()
