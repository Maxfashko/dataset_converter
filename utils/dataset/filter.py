
from utils.parser.container import Annotation, AnnotationsContainer, BBox


class Filter(object):
    """filters objects of annotations_container type by specified rules"""
    def __init__(self, annotations_container, cfg):
        super(Filter, self).__init__()
        self.annotations_container = annotations_container

    def filter_out(self):
        '''filtration'''
        return self.annotations_container
