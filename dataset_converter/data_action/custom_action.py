from abc import ABC
from abc import abstractmethod


class CustomAction(ABC):
    def __init__(self, **kwargs):
        super(CustomAction, self).__init__()

    @classmethod
    def init_process(cls, fun):
        def wrapper(self, *args, **kwargs):
            print(f'start action {self.__class__.__name__}...')
            ret = fun(self, *args, **kwargs)
            print(f'finish action {self.__class__.__name__}')
            return ret
        return wrapper

    @abstractmethod
    def process(self):
        pass
