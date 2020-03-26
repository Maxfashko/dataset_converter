import os
import sys
import math
import uuid
import os.path as osp

import cv2
import numpy as np
from tqdm import tqdm

from .custom_action import CustomAction
from dataset_converter.parser.container import AnnotationsContainer


class MakeCropsAction(CustomAction):
    """
    Сreates crop from images with objects. Crops are saved in a temporary folder.
    In the future, when calling the convert function, crop will be used instead of whole images
    """
    def __init__(self, min_height, crop_width=None, crop_height=None):
        super(CustomAction, self).__init__()
        self.min_height = min_height
        self.crop_width = crop_width
        self.crop_height = crop_height

        # make folder for image crops
        self.image_path = osp.join('/tmp', str(uuid.uuid4()))
        self.make_tmp_dir()

    def check_path(self):
        if os.path.exists(self.image_path):
            return True
        return False

    def make_tmp_dir(self, rewrite=True):
        if self.check_path():
            if not rewrite:
                print(f'directory {self.image_path} already exists!')
                sys.exit(-1)
            else:
                shutil.rmtree(self.image_path)

        os.makedirs(self.image_path)

        print(f'temporary folder created {self.image_path}')

    def make_crop(self, img_fn, an):
        crop_image = cv2.imread(img_fn)
        crop_image = crop_image[an.bbox.y1:an.bbox.y2, an.bbox.x1:an.bbox.x2]

        if self.crop_width is not None and self.crop_height is not None:
            crop_image = cv2.resize(crop_image, (self.crop_width, self.crop_height))

        path = osp.join(self.image_path, str(uuid.uuid4()) + '.jpg')
        cv2.imwrite(path, crop_image)
        return path

    @CustomAction.init_process
    def process(self, annotations_container):
        annotations_container_new = AnnotationsContainer()

        with tqdm(total=len(annotations_container)) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                annotations = []

                for idx, an in enumerate(annts):
                    if an.bbox.height >= self.min_height:
                        try:
                            crop_img_name = self.make_crop(img_fn, an)
                            annotations_container_new.add_data(
                                annotations=[an],
                                annotation_filename=None,
                                image_filename=crop_img_name
                            )
                        except Exception as e:
                            pass

                pbar.update(1)
        return annotations_container_new
