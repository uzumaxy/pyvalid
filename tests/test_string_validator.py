import unittest
from pyvalid.validators import StringValidator


class StringValidatorTestCase(unittest.TestCase):

    def test_min_len(self):
        validator = StringValidator(min_len=2)
        self.assertTrue(validator('Python'))
        self.assertTrue(validator('Py'))
        self.assertFalse(validator('P'))

    def test_max_len(self):
        validator = StringValidator(max_len=6)
        self.assertTrue(validator(str()))
        self.assertTrue(validator('Python'))
        self.assertFalse(validator('Python3'))

    def test_in_range(self):
        validator = StringValidator(
            in_range=['CPython', 'PyPy', 'IronPython', 'Jython', 'Cython']
        )
        self.assertTrue(validator('PyPy'))
        self.assertTrue(validator('Cython'))
        self.assertFalse(validator('Ruby'))

    def test_not_in_range(self):
        validator = StringValidator(
            not_in_range=['CPython', 'PyPy', 'IronPython', 'Jython', 'Cython']
        )
        self.assertTrue(validator('Ruby'))
        self.assertTrue(validator('Java'))
        self.assertFalse(validator('CPython'))

    def test_mixed(self):
        validator = StringValidator(
            min_len=6, max_len=64,
            not_in_range=['password', 'qwerty', '123456789', 'sunshine'],
        )
        self.assertTrue(validator('Super_Mega_Strong_Password_2000'))
        self.assertTrue(validator('_'*6))
        self.assertFalse(validator('_'*3))
        self.assertFalse(validator('_'*128))
        self.assertFalse(validator('sunshine'))


if __name__ == '__main__':
    unittest.main()