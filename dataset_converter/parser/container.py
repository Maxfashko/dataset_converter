import os.path as osp

import numpy as np


def get_name(path):
    pass


class BBox(object):
    """docstring for BBox"""
    def __init__(self, **kwargs):
        super(BBox, self).__init__()
        self.x1 = int(kwargs['x1'])
        self.x2 = int(kwargs['x2'])
        self.y1 = int(kwargs['y1'])
        self.y2 = int(kwargs['y2'])
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.cx = int(self.x1 + (self.width / 2))
        self.cy = int(self.y1 + (self.height / 2))
        self.test_correct()

    def reinit(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.cx = self.x1 + (self.width / 2)
        self.cy = self.y1 + (self.height / 2)

    def test_correct(self):
        if self.width < 0:
            self.reinit(x1=self.x2, y1=self.y1, x2=self.x1, y2=self.y2)
        if self.height < 0:
            self.reinit(x1=self.x1, y1=self.y2, x2=self.x2, y2=self.y1)


    def transform_range(self, w, h):
        # bounds should be in range [0, 1]

        x1 = self.x1 / w
        x2 = self.x2 / w
        y1 = self.y1 / h
        y2 = self.y2 / h
        self.reinit(x1, y1, x2, y2)
        self.test_correct()

    def rescale_with_pointf(self, pointf):
        """ pointf: float """

        self.x1 = int(self.x1 / pointf)
        self.y1 = int(self.y1 / pointf)
        self.x2 = int(self.x2 / pointf)
        self.y2 = int(self.y2 / pointf)
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.cx = self.x1 + (self.width / 2)
        self.cy = self.y1 + (self.height / 2)

    # сделано по уебански!!!
    def rescale_with_point2f(self, point2f, mode='div'):
        """ point2f: Point2f(x,y) """

        if mode == 'div':
            self.x1 = int(self.x1 / point2f.x)
            self.y1 = int(self.y1 / point2f.y)
            self.x2 = int(self.x2 / point2f.x)
            self.y2 = int(self.y2 / point2f.y)
        elif mode == 'mul':
            self.x1 = int(self.x1 * point2f.x)
            self.y1 = int(self.y1 * point2f.y)
            self.x2 = int(self.x2 * point2f.x)
            self.y2 = int(self.y2 * point2f.y)
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.cx = int(self.x1 + (self.width / 2))
        self.cy = int(self.y1 + (self.height / 2))

    def expand_with_percent(self, x_percent, y_percent):
        """ расширить область текущего bbox на заданный процент """

        assert 100 > x_percent or 100 > y_percent

        w_expand = self.width + (self.width / 100 * x_percent)
        h_expand = self.height + (self.height / 100 * y_percent)

        self.x1 = int(self.cx - (w_expand / 2))
        self.y1 = int(self.cy - (h_expand / 2))
        self.x2 = int(self.cx + (w_expand / 2))
        self.y2 = int(self.cy + (h_expand / 2))
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.cx = int(self.x1 + (self.width / 2))
        self.cy = int(self.y1 + (self.height / 2))

    def set_origin(self, origin_bbox):
        """задать начало координат текущему bbox при помощи другого bbox"""
        """ origin_bbox: BBox(x1, x2, y1, y2) """

        self.x1 = self.x1 + origin_bbox.x1
        self.y1 = self.y1 + origin_bbox.y1
        self.x2 = self.x2 + origin_bbox.x1
        self.y2 = self.y2 + origin_bbox.y1

    def to_numpy(self, dtype='uint8'):
        return np.array([self.x1, self.y1, self.x2, self.y2], dtype=dtype)


class Annotation:
    def __init__(self, **kwargs):
        self.bbox = kwargs.get('bbox')
        self.label = kwargs.get('label')
        self.segmentations = kwargs.get('segmentations')


class AnnotationObject:
    def __init__(self, **kwargs):

        # contained elements of Annotation
        self.annotations = kwargs.get('annotations'),
        self.image_filename = kwargs.get('image_filename'),
        self.annotation_filename = kwargs.get('annotation_filename')


class AnnotationsContainer:
    def __init__(self):

        # contained elements of AnnotationObject
        self._annotations_container = []

    def get_data(self):
        for idx, obj in enumerate(self._annotations_container):
            yield idx, obj.annotations[0], obj.image_filename[0], obj.annotation_filename

    def mapping_labels_to_int(self):
        L = []

        for obj in self._annotations_container:
            for ant in obj.annotations[0]:
                L.append(ant.label)

        return dict(zip(set(L), range(len(L))))


    def get_len(self):
        return len(self._annotations_container)

    def add_data(self, annotations, image_filename, annotation_filename):
        self._annotations_container.append(
            AnnotationObject(
                annotations=annotations,
                image_filename=image_filename,
                annotation_filename=annotation_filename
            )
        )
