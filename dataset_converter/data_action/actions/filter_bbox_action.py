import os
import math
import os.path as osp

import numpy as np
from tqdm import tqdm

from .custom_action import CustomAction
from dataset_converter.parser.container import AnnotationsContainer


class FilterBBoxAction(CustomAction):
    def __init__(self, min_area, parser=None):
        super(CustomAction, self).__init__()
        self.min_area = min_area

    @CustomAction.init_process
    def process(self, annotations_container):
        annotations_container_new = AnnotationsContainer()

        with tqdm(total=len(annotations_container)) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                annotations = []

                for an in annts:
                    if an.bbox.width * an.bbox.height >= self.min_area:
                        annotations.append(an)
                    else:
                        print('min_area!', an.bbox.width * an.bbox.height)

                if annotations:
                    annotations_container_new.add_data(
                        annotations=annotations,
                        image_filename=img_fn,
                        annotation_filename=None
                    )

                pbar.update(1)
        return annotations_container_new
