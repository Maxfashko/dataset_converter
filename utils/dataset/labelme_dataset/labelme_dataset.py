import shutil
from glob import glob
import os.path as osp
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import imagesize
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from utils.dataset.custom_dataset import CustomDataset
from utils.dataset.labelme_dataset.xmlparser import XmlParser
from utils.parser.container import Annotation, AnnotationsContainer, BBox
from utils.dataset.labelme_dataset.labelme_struct_dataset import LabelmeStructDataset


"""
labelme annotation tool
for example structure:

-Labelme_annotations
    |-Annotations
        |-project1
            -1.xml
            -...
            -n.xml
        |-project2
    |-Images
        |-project1
            -1.jpg
            -...
            -n.jpg
        |-project2
    |-Info
        |-project1
            -labels_set.json
        |-project2
    |-Masks
        |-project1
        |-project2
    |-Scribbles

cfg params:
    data_root='Labelme_annotations'
    dir_name=project1
"""

class LabelmeDataset(CustomDataset):
    """docstring for LabelmeDataset"""
    def __init__(self, data_root, dir_name, labels_params):
        super(CustomDataset, self).__init__()
        self.data_root = data_root
        self.dir_name = dir_name
        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = LabelmeStructDataset(
            data_root=self.data_root, dir_name=self.dir_name
        )

    def parse(self):
        pass

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        if not self.struct.check_struct_path():
            self.struct.make_struct_path()

        # create project folders
        self.struct.make_project_path()

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                (w, h), d = imagesize.get(img_fn), 3

                xml_annot = XmlParser()
                xml_annot.set_filename_root(f'{idx}{self.struct.image_ext}')
                xml_annot.set_size_root(width=w, height=h, depth=d)

                for annt in annts:
                    xml_annot.add_sub_object(name=annt.label, bbox=annt.bbox)

                # write annot
                xml_annot.write_root(self.struct.get_annotation_file(idx))

                # write image
                shutil.copy(img_fn, self.struct.get_image_file(idx))

                pbar.update(1)
