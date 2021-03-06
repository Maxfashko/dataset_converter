import sys
import copy

import six
from dataset_converter import dataset as parent


def is_str(x):
    """Whether the input is an string instance."""
    return isinstance(x, six.string_types)


class Provider:
    @staticmethod
    def get_dataset(data_cfg):
        data_info = copy.deepcopy(data_cfg)

        dataset_type = data_info.pop('type')
        try:
            if is_str(dataset_type):
                dataset_type = getattr(parent, dataset_type)
            return dataset_type(**data_info)
        except Exception as e:
            print(e)
