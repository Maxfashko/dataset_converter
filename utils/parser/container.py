import os.path as osp

def get_name(path):
    pass


class BBox(object):
    """docstring for BBox"""
    def __init__(self, **kwargs):
        super(BBox, self).__init__()
        self.x1 = kwargs['x1']
        self.x2 = kwargs['x2']
        self.y1 = kwargs['y1']
        self.y2 = kwargs['y2']


class Annotation:
    def __init__(self, **kwargs):
        self.bbox = kwargs.get('bbox')
        self.label = kwargs.get('label')
        self.segmentations = kwargs.get('segmentations')


class AnnotationObject:
    def __init__(self, **kwargs):
        self.annotations = kwargs.get('annotations'),
        self.image_filename = kwargs.get('image_filename'),
        self.annotation_filename = kwargs.get('annotation_filename')


class AnnotationsContainer:
    def __init__(self):
        self._annotations_container = []

    def get_data(self):
        for idx, annotation_object in enumerate(self._annotations_container):
            yield idx, \
                annotation_object.annotations[0], \
                annotation_object.image_filename[0], \
                annotation_object.annotation_filename


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
