from unittest import TestCase

from schemify import validate, ValidationError, opt, anything

__all__ = ()

class TestSchemify(TestCase):

    def test_simple(self):
        self.assertEqual(validate(int, 1), 1)
        self.assertEqual(validate(int, "1"), 1)
        self.assertEqual(validate(str, "1"), "1")
        self.assertEqual(validate([int], ["1"]), [1])
        self.assertEqual(validate((int, int), ("1", "2")), (1, 2))
        self.assertEqual(
            validate({"a": int, "b": str}, {"a": "1", "b": "c"}),
            {"a": 1, "b": "c"})
        self.assertEqual(validate(bool, 1), True)
        self.assertEqual(validate(bool, "1"), True)

    def test_tuple(self):
        self.assertEqual(validate((int, int), (1, 2)), (1, 2))
        self.assertEqual(validate((int, str), (1, '2')), (1, '2'))
        self.assertEqual(validate((int, str), ('1', '2')), (1, '2'))
        self.assertRaises(ValidationError, validate, (int, str), ('s', 'a'))
        self.assertRaises(ValidationError, validate, (int, str), (1,))

    def test_list(self):
        self.assertEqual(validate([int], ['1', '2']), [1, 2])
        self.assertEqual(validate([str], ['1', '2']), ['1', '2'])

    def test_dict(self):
        self.assertEqual(validate({'a': int}, {'a': '1'}), {'a': 1})
        self.assertEqual(validate({'a': int}, {'a': '1', 'b': '2'}), {'a': 1})
        self.assertRaises(ValidationError, validate, {'a': int}, {})
        self.assertRaises(ValidationError, validate, {'a': int}, {'b': '1'})
        self.assertRaises(ValidationError, validate, {'a': int}, {'a': 's'})

        self.assertEqual(validate({'a': opt(int)}, {}), {})
        self.assertEqual(validate({'a': opt(int)}, {'a': '1'}), {'a': 1})
        self.assertEqual(validate({'a': opt(int, 3)}, {}), {'a': 3})

    def test_namedtuple(self):
        from collections import namedtuple
        X = namedtuple('X', 'x y')
        Y = namedtuple('Y', 'z')
        schema = X(x=str, y=Y(z=int))

        data = {'x': 'id', 'y': {'z': 3}}
        self.assertEqual(validate(schema, data), X('id', Y(3)))

        data = {'x': 'id', 'y': {'z': 'a'}}
        self.assertRaises(ValidationError, validate, schema, data)

    def test_anything(self):
        self.assertEqual(validate(anything, 1), 1)
        self.assertEqual(validate(anything, 'a'), 'a')
        self.assertEqual(validate({'a': anything}, {'a': 1}), {'a': 1})
        self.assertEqual(validate({'a': anything}, {'a': '1'}), {'a': '1'})
