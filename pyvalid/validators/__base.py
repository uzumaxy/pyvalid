from abc import ABCMeta, abstractmethod
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

from six import with_metaclass

from pyvalid import accepts


class Validator(Callable):

    @accepts(object, Callable)
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


class AbstractValidator(with_metaclass(ABCMeta, Validator)):

    @property
    @abstractmethod
    def checkers(self):
        raise NotImplementedError

    def __call__(self, val):
        is_valid = False
        if self.allowed_types is None or isinstance(val, self.allowed_types):
            is_valid = self._check(val)
        return is_valid

    def __init__(self, **kwargs):
        self.allowed_types = kwargs.get('allowed_types', None)
        Validator.__init__(self, self)
        for checker_func, checker_args in list(self.checkers.items()):
            try:
                to_del = checker_args[0] is None
            except (IndexError, TypeError):
                to_del = True
            if to_del:
                del self.checkers[checker_func]

    def _check(self, val):
        valid = True
        for checker_func, checker_args in self.checkers.items():
            valid = checker_func(val, *checker_args)
            if not valid:
                break
        return valid
