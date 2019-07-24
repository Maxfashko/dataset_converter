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

from dataset_converter.data_action.custom_action import CustomAction
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox


class SliceObj:
    def __init__(self, tile, boxes, labels):
        self.tile = tile
        self.boxes = boxes
        self.labels = labels


class ImageSlicer(CustomAction):
    """
    Helper class to slice image into tiles and merge them back
    """
    def __init__(self, tile_size, tile_step=0, image_margin=0):
        super(CustomAction, self).__init__()

        """
        :param image_shape: Shape of the source image (H, W)
        :param tile_size: Tile size (Scalar or tuple (H, W)
        :param tile_step: Step in pixels between tiles (Scalar or tuple (H, W))
        :param image_margin:
        """
        self.tile_size = tile_size
        self.tile_step = tile_step
        self.image_margin = image_margin

        if isinstance(self.tile_size, (tuple, list)):
            assert len(self.tile_size) == 2
            self.tile_size = int(self.tile_size[0]), int(tile_size[1])
        else:
            self.tile_size = int(tile_size), int(tile_size)

        if isinstance(tile_step, (tuple, list)):
            assert len(tile_step) == 2
            self.tile_step = int(tile_step[0]), int(tile_step[1])
        else:
            self.tile_step = int(tile_step), int(tile_step)

        if self.tile_step[0] < 1 or self.tile_step[0] > self.tile_size[0]:
            raise ValueError()
        if self.tile_step[1] < 1 or self.tile_step[1] > self.tile_size[1]:
            raise ValueError()

        self.overlap = [
            self.tile_size[0] - self.tile_step[0],
            self.tile_size[1] - self.tile_step[1],
        ]

        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0


    def init_params(self, image_shape):
        self.image_height = image_shape[0]
        self.image_width = image_shape[1]

        if self.image_margin == 0:
            # In case margin is not set, we compute it manually

            nw = max(1, math.ceil((self.image_width - self.overlap[1]) / self.tile_step[1]))
            nh = max(1, math.ceil((self.image_height - self.overlap[0]) / self.tile_step[0]))

            extra_w = self.tile_step[1] * nw - (self.image_width - self.overlap[1])
            extra_h = self.tile_step[0] * nh - (self.image_height - self.overlap[0])

            self.margin_left = extra_w // 2
            self.margin_right = extra_w - self.margin_left
            self.margin_top = extra_h // 2
            self.margin_bottom = extra_h - self.margin_top

        else:
            if (self.image_width - self.overlap[1] + 2 * image_margin) % self.tile_step[1] != 0:
                raise ValueError()

            if (self.image_height - self.overlap[0] + 2 * image_margin) % self.tile_step[0] != 0:
                raise ValueError()

            self.margin_left = image_margin
            self.margin_right = image_margin
            self.margin_top = image_margin
            self.margin_bottom = image_margin

        crops = []
        bbox_crops = []

        for y in range(0, self.image_height + self.margin_top + self.margin_bottom - self.tile_size[0] + 1, self.tile_step[0]):
            for x in range(0, self.image_width + self.margin_left + self.margin_right - self.tile_size[1] + 1, self.tile_step[1]):
                crops.append((x, y, self.tile_size[1], self.tile_size[0]))
                bbox_crops.append((x - self.margin_left, y - self.margin_top, self.tile_size[1], self.tile_size[0]))

        self.crops = np.array(crops)
        self.bbox_crops = np.array(bbox_crops)

    @CustomAction.init_process
    def process(self, annotations_container):
        annotations_container_new = AnnotationsContainer()

        tmp_img_path = '/tmp/image_slicer_image/'
        if not osp.exists(tmp_img_path):
            os.makedirs(tmp_img_path)

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                img = cv2.imread(img_fn)
                self.init_params(image_shape = img.shape)

                # convert annotations to np
                boxes = []
                labels = []
                for an in annts:
                    boxes.append([an.bbox.x1, an.bbox.y1, an.bbox.x2, an.bbox.y2])
                    labels.append(an.label)
                boxes = np.asarray(boxes)
                labels = np.asarray(labels)

                # slice img and annotation
                slice_objects = [tile for tile in self.split(img, boxes, labels)]

                # parse slice_objects to AnnotationsContainer
                for obj in slice_objects:

                    # save current tile to tmp folder
                    img_name = osp.join(tmp_img_path, str(idx)+'.jpg')
                    cv2.imwrite(img_name, obj.tile)

                    annotations = []

                    for box, label in zip(obj.boxes, obj.labels):
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

                pbar.update(1)

        return annotations_container_new

    def split_annotations(self, boxes, labels, crd):
        x, y, tile_width, tile_height = crd

        # filter bbox in area
        patch = np.array((int(x), int(y), int(x + tile_width), int(y + tile_height)))

        center = (boxes[:, :2] + boxes[:, 2:]) / 2
        mask = (center[:, 0] > patch[0]) * (center[:, 1] > patch[1]) * (center[:, 0] < patch[2]) * (center[:, 1] < patch[3])
        if not mask.any():
            return False, None, None

        boxes = boxes[mask]
        labels = labels[mask]

        # adjust boxes
        boxes[:, 2:] = boxes[:, 2:].clip(max=patch[2:])
        boxes[:, :2] = boxes[:, :2].clip(min=patch[:2])
        boxes -= np.tile(patch[:2], 2)
        return True, boxes, labels

    def split(self, image, boxes, labels, border_type=cv2.BORDER_CONSTANT, value=0):
        assert image.shape[0] == self.image_height
        assert image.shape[1] == self.image_width

        orig_shape_len = len(image.shape)
        image = cv2.copyMakeBorder(image, self.margin_top, self.margin_bottom, self.margin_left, self.margin_right, borderType=border_type, value=value)

        # This check recovers possible lack of last dummy dimension for single-channel images
        if len(image.shape) != orig_shape_len:
            image = np.expand_dims(image, axis=-1)

        # list contained elem of SliceObj class
        slice_objects = []
        for x, y, tile_width, tile_height in self.crops:
            tile = image[y:y + tile_height, x:x + tile_width].copy()
            assert tile.shape[0] == self.tile_size[0]
            assert tile.shape[1] == self.tile_size[1]

            ret, mask_boxes, mask_labels = self.split_annotations(boxes, labels, [x, y, tile_width, tile_height])
            if not ret:
                continue

            slice_objects.append(SliceObj(tile=tile, boxes=mask_boxes, labels=mask_labels))

        return slice_objects

    @property
    def target_shape(self):
        target_shape = self.image_height + self.margin_bottom + self.margin_top, self.image_width + self.margin_right + self.margin_left
        return target_shape
