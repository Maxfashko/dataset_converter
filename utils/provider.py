import copy

from utils import dataset
from utils.config.obj_from_dict import obj_from_dict


class Provider:
    @staticmethod
    def get_dataset(data_cfg):
        data_info = copy.deepcopy(data_cfg)
        print(data_info)
        print(type(data_info))

        print(dataset)
        dset = obj_from_dict(data_info, dataset)
        print(dset)
