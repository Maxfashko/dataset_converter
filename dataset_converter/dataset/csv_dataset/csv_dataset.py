import sys
import shutil
from glob import glob
import os.path as osp

import imagesize
from tqdm import tqdm

from dataset_converter.dataset import CustomDataset
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox
from dataset_converter.dataset import CsvStructDataset

"""

"""


class CsvDataset(CustomDataset):
    """docstring for LabelmeDataset"""

    def __init__(self, params=None, images=None, annotations=None, **kwargs):
        super(CsvDataset, self).__init__()
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.annotations = annotations
        self.images = images

        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = CsvStructDataset(
            data_root=self.data_root,
            dir_name=self.dir_name,
            annotations=self.annotations
        )

    @CustomDataset.init_parse
    def parse(self):
        raise NotImplementedError

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        self.struct.make_struct()

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():

                for annt in annts:
                    self.struct.add_data(img_fn, annt.bbox, annt.label)

                pbar.update(1)

            # write annotations with pandas
            self.struct.dump()
