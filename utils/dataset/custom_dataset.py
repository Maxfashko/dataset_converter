from abc import ABC
from abc import abstractmethod


class CustomDataset(ABC):
    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def convert(self):
        pass
