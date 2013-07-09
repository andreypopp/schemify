# schemify

Simple schema validation for Python.

## Installation

Via easy\_install:

    % easy_install schemify

or via pip:

    % pip install schemify

## Usage

Compose schemas from builtins — `int`, `str`, `bool`, `list`, `dict` to validate
and convert structures to desired datatypes:

    >>> from schemify import validate

    >>> schema = {'a': {'b': [int]}, 'c': str}
    >>> data = {'a': {'b': ['1']}, 'c': 'c'}

    >>> validate(schema, data)
    {'a': {'b': [1]}, 'c': 'c'}

dictionaries can have optional keys and you can supply default values for such
keys:

    >>> schema = {'a': opt(int, default=1)}
    >>> data = {}
    >>> validate(schema, data)
    {'a': 1}

you can also use `nameduple`:

    >>> from collections import namedtuple
    >>> X = namedtuple('X', 'a y')
    >>> Y = namedtuple('Y', 'b c')

    >>> schema = X(int, Y(int, str))
    >>> data = {'a': 1, 'y': {'b': 2, 'c': 'zzz'}}

    >>> validate(schema, data)
    X(1, Y(2, 'zzz'))

Use `anything` validator for suppressing validation at some point:

    >>> from schemify import anything

    >>> schema = {'a': anything}

    >>> validate(schema, {'a': {}})
    {'a': {}}
    >>> validate(schema, {'a': 1})
    {'a': 1}

To provide new validator just use a function which converts value to a desired
datatype and raises `ValidationError` on invalid input:

    >>> from schemify import ValidationError
    >>> import re
    >>> alphanum_re = re.compile('^[a-zA-Z]+$')
    >>> def alphanum(v):
    ...   if not alphanum_re.match(v):
    ...     raise ValidationError('should contain only alphanum chars')
    ...   return v

and use it:

    >>> schema = {'a': alphanum}
    >>> data = {'a': 'somestring'}

    >>> validate(schema, data)
    {'a': 'somestring'}
