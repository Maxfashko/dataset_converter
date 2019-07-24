import sys
import copy

import six
from dataset_converter import data_action as parent
from dataset_converter.config.obj_from_dict import obj_from_dict


def is_str(x):
    """Whether the input is an string instance."""
    return isinstance(x, six.string_types)


class Provider:
    @staticmethod
    def get_action(data_cfg):
        params = copy.deepcopy(data_cfg)

        action_type = params.pop('type')

        try:
            if is_str(action_type):
                action_type = getattr(parent, action_type)
            return action_type(**params)
        except Exception as e:
            print(e)
