import sys
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
    def __init__(self, data_root, dir_name):
        super(CustomDataset, self).__init__()
        self.data_root = data_root
        self.dir_name = dir_name
        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = LabelmeStructDataset(
            data_root=self.data_root, dir_name=self.dir_name
        )

    @CustomDataset.init_parse
    def parse(self):
        if not self.struct.check_project_path():
            print(f'path not exists! {self.data_path}')
            sys.exit()

        def parse_points(polygon):
            d = {'x':set(), 'y':set()}

            for pt in polygon.findall("pt"):
                d['x'].add(int(float(pt.find('x').text)))
                d['y'].add(int(float(pt.find('y').text)))

            x1 = min(d['x'])
            y1 = min(d['y'])
            x2 = max(d['x'])
            y2 = max(d['y'])

            return x1, y1, x2, y2


        annotations_container = AnnotationsContainer()
        filenames = list(glob(f'{self.struct.annot_dir_project}/*{self.struct.annot_ext}'))

        with tqdm(total=len(filenames)) as pbar:
            for fn in filenames:
                annotations = []
                basename, _ = osp.splitext(osp.basename(fn))

                tree = ElementTree.parse(fn)
                root = tree.getroot()

                for obj in root.findall('object'):
                    if obj.find('type').text == 'bounding_box':
                        polygon = obj.find('polygon')
                        x1, y1, x2, y2 = parse_points(polygon)

                        annotations.append(
                            Annotation(
                                bbox=BBox(x1=x1, y1=y1, x2=x2, y2=y2),
                                label=obj.find("name").text
                            )
                        )

                annotations_container.add_data(
                    annotations=annotations,
                    image_filename=self.struct.get_image_file(basename),
                    annotation_filename=self.struct.get_annotation_file(basename)
                )
                pbar.update(1)
        return annotations_container

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
