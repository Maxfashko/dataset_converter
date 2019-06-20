from abc import ABC
from abc import abstractmethod


class CustomDataset(ABC):
    def __init__(self, data_path):
        super(CustomDataset, self).__init__(data_path)
        self.data_path = data_path

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def convert(self):
        pass
