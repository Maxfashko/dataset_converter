
import os
import math
import os.path as osp

import numpy as np
from tqdm import tqdm

from .custom_action import CustomAction
from dataset_converter.parser.container import AnnotationsContainer


class FilterLabelsAction(CustomAction):
    def __init__(self, allowed_labels, labels_mapping):
        super(CustomAction, self).__init__()
        self.allowed_labels = allowed_labels
        self.labels_mapping = labels_mapping

    @CustomAction.init_process
    def process(self, annotations_container):
        annotations_container_new = AnnotationsContainer()

        count = 0
        with tqdm(total=len(annotations_container)) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                annotations = []

                for an in annts:

                    # filter labels
                    if an.label in self.allowed_labels:
                        annotations.append(an)

                    # mapping labels
                    if an.label in self.labels_mapping:
                        an.label = self.labels_mapping[an.label]
                        annotations.append(an)

                if annotations:
                    annotations_container_new.add_data(
                        annotations=annotations,
                        image_filename=img_fn,
                        annotation_filename=None
                    )

                pbar.update(1)
        return annotations_container_new
