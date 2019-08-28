import sys
import shutil
from glob import glob
import os.path as osp
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import imagesize
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from dataset_converter.dataset.custom_dataset import CustomDataset
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox
from dataset_converter.dataset.coco_dataset.coco_struct_dataset import CocoStructDataset


class CocoDataset(CustomDataset):
    def __init__(self, params=None, images=None, annotations=None, **kwargs):
        super(CustomDataset, self).__init__()
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.images = images
        self.params = params
        self.annotations = annotations

        self.data_path = osp.join(self.data_root, self.dir_name)
        self.params = params
        self.struct = CocoStructDataset(
            path=self.data_path,
            images=self.images,
            annotations=self.annotations)

    @CustomDataset.init_parse
    def parse(self):
        if not self.struct.check_path():
            print(f'path not exists! {self.data_path}')
            sys.exit()

        annotations_container = AnnotationsContainer()

        with tqdm(total=len(self.struct)) as pbar:
            for annt_ids, img_id in self.struct.provider():
                annotations = []

                for annt_id in annt_ids:
                    annotations.append(
                        Annotation(
                            bbox=self.struct.get_bbox(annt_id),
                            label=self.struct.get_label(annt_id)
                        )
                    )

                annotations_container.add_data(
                    annotations=annotations,
                    image_filename=self.struct.get_image_name(img_id),
                    annotation_filename=None
                )
                pbar.update(1)
        return annotations_container

    def create_imagesets(self, idx, test_size=0.2, seed=42):
        ''' create ImageSets train/val '''

        try:
            numbers = [x for x in range(0, idx)]
            train, test, _, _ = train_test_split(numbers, numbers, test_size=test_size, random_state=seed)

            self.struct.make_image_list(train, 'train')
            self.struct.make_image_list(test, 'test')
        except Exception as e:
            raise

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        pass
