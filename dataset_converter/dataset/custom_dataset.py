from abc import ABC
from abc import abstractmethod


class CustomDataset(ABC):
    def __init__(self, **kwargs):
        super(CustomDataset, self).__init__()
        self.data_root = data_root
        self.dir_name = dir_name

    @classmethod
    def init_parse(cls, fun):
        def wrapper(self, *args, **kwargs):
            print('start parse...')
            ret = fun(self, *args, **kwargs)
            print('parse completed')
            return ret
        return wrapper

    @classmethod
    def init_convert(cls, fun):
        def wrapper(self, *args, **kwargs):
            print('start convert...')
            ret = fun(self, *args, **kwargs)
            print('convert completed')
            return ret
        return wrapper

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def convert(self):
        pass
