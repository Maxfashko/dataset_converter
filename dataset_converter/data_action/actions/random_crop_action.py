"""Implementation of tile-based inference allowing to predict huge images that does not fit into GPU memory entirely
in a sliding-window fashion and merging prediction mask back to full-resolution.
"""
import os
import math
import os.path as osp
from typing import List

import cv2
import numpy as np
from tqdm import tqdm
from albumentations import *

from .custom_action import CustomAction
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox


class RandomCropAction(CustomAction):
    """
    Helper class to augmentation data
    """
    def __init__(self, width, height, n_crops, min_area, max_iters=50, parser=None):
        super(CustomAction, self).__init__()
        self.min_area = min_area
        self.width = width
        self.height = height
        self.n_crops = n_crops
        self.max_iters = max_iters
        self.augmentations=[
            RandomCrop(self.height, self.width, always_apply=False, p=1.0)
        ]

        self.get_aug = self.init_aug(self.augmentations)

    def init_aug(self, aug, min_visibility=0.):
        return Compose(
            aug,
            # bbox_params={'format': 'pascal_voc', 'min_area': min_area, 'min_visibility': min_visibility, 'label_fields': ['category_id']}
            bbox_params={'format': 'pascal_voc', 'min_area': self.min_area, 'min_visibility': min_visibility, 'label_fields': ['labels']}
        )

    @CustomAction.init_process
    def process(self, annotations_container):
        annotations_container_new = AnnotationsContainer()

        tmp_img_path = '/tmp/random_crop_action/'
        if not osp.exists(tmp_img_path):
            os.makedirs(tmp_img_path)

        count = 0
        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                img = cv2.imread(img_fn)

                boxes = []
                labels = []
                crop_boxes = []
                crop_labels = []
                crop_images = []

                for an in annts:
                    boxes.append([an.bbox.x1, an.bbox.y1, an.bbox.x2, an.bbox.y2])
                    labels.append(an.label)

                for step in range(self.max_iters):
                    try:
                        annotations = {'image': img, 'bboxes': boxes, 'labels': labels}
                        augmented = self.get_aug(**annotations)
                    except Exception as e:
                        continue

                    if len(augmented['bboxes']) == 0:
                        continue

                    crop_images.append(augmented['image'])
                    crop_boxes.append(augmented['bboxes'])
                    crop_labels.append(augmented['labels'])

                    if len(crop_images) == self.n_crops:
                        break

                for img, labels, boxes in zip(crop_images, crop_labels, crop_boxes):
                    # save current tile to tmp folder
                    img_name = osp.join(tmp_img_path, str(count)+'.png')
                    cv2.imwrite(img_name, img)

                    annotations = []

                    for box, label in zip(boxes, labels):
                        box=list(map(lambda x:int(x), box))
                        annotations.append(
                            Annotation(
                                bbox=BBox(x1=box[0], y1=box[1], x2=box[2], y2=box[3]),
                                label=label
                            )
                        )

                    annotations_container_new.add_data(
                        annotations=annotations,
                        image_filename=img_name,
                        annotation_filename=None
                    )

                    count += 1
                pbar.update(1)
        return annotations_container_new
