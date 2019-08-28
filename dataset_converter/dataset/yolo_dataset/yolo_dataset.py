import sys
import shutil
from glob import glob
import os.path as osp

import imagesize
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from dataset_converter.dataset.yolo_dataset.yolo_struct_dataset import YoloStructDataset
from dataset_converter.dataset.custom_dataset import CustomDataset
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox


class YoloDataset(CustomDataset):
    def __init__(self, params=None, images=None, annotations=None, **kwargs):
        super(CustomDataset, self).__init__()
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.images = images
        self.params = params
        self.annotations = annotations

        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = YoloStructDataset(
            path=self.data_path,
            images=self.images,
            annotations=self.annotations)

    @CustomDataset.init_parse
    def parse(self):
        return NotImplemented

    def create_imagesets(self, idx, test_size=0.2, seed=42):
        ''' create ImageSets train/val '''

        if self.params is not None:
            test_size = self.params.train_test_split.test
            seed = self.params.train_test_split.seed

        try:
            numbers = [self.struct.get_image_file(x) for x in range(0, idx)]
            train, test, _, _ = train_test_split(numbers, numbers, test_size=test_size, random_state=seed)

            self.struct.make_image_list(train, 'train')
            self.struct.make_image_list(test, 'test')
        except Exception as e:
            raise

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        self.struct.make_struct()

        labels_mapping = annotations_container.mapping_labels_to_int()

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                (w, h) = imagesize.get(img_fn)

                # write annot
                with open(self.struct.get_annotation_file(idx), 'a') as f:
                    for annt in annts:
                        annt.bbox.transform_range(w, h)
                        f.write(f'{labels_mapping[annt.label]} {annt.bbox.cx} {annt.bbox.cy} {annt.bbox.width} {annt.bbox.height}\n')

                # write image
                shutil.copy(img_fn, self.struct.get_image_file(idx))

                pbar.update(1)

        # make txt list with train/test filenames
        self.create_imagesets(idx)
