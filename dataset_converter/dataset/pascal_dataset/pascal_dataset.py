import sys
import shutil
from glob import glob
import os.path as osp
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import imagesize
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from dataset_converter.dataset.custom_dataset import CustomDataset
from dataset_converter.dataset.pascal_dataset.xmlparser import XmlParser
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox
from dataset_converter.dataset.pascal_dataset.pascal_struct_dataset import PascalStructDataset


class PascalDataset(CustomDataset):
    def __init__(self, data_root, dir_name):
        super(CustomDataset, self).__init__()
        self.data_root = data_root
        self.dir_name = dir_name
        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = PascalStructDataset(path=self.data_path)

    @CustomDataset.init_parse
    def parse(self):
        if not self.struct.check_path():
            print(f'path not exists! {self.data_path}')
            sys.exit()

        annotations_container = AnnotationsContainer()
        filenames = list(glob(f'{self.struct.annot_dir}/*{self.struct.annot_ext}'))

        with tqdm(total=len(filenames)) as pbar:
            for fn in filenames:
                annotations = []
                basename, _ = osp.splitext(osp.basename(fn))

                tree = ElementTree.parse(fn)
                root = tree.getroot()

                for obj in root.findall('object'):
                    bbox = obj.find('bndbox')

                    annotations.append(
                        Annotation(
                            bbox=BBox(
                                x1=float(bbox.find("xmin").text),
                                y1=float(bbox.find("ymin").text),
                                x2=float(bbox.find("xmax").text),
                                y2=float(bbox.find("ymax").text)),
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

    def create_imagesets(self, idx, test_size=0.2, seed=42):
        ''' create ImageSets train/val '''

        try:
            numbers = [x for x in range(0, idx)]
            train, test, _, _ = train_test_split(numbers, numbers, test_size=test_size, random_state=seed)

            self.struct.make_image_list(train, 'train')
            self.struct.make_image_list(test, 'test')
        except Exception as e:
            raise

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        if not self.struct.check_path():
            self.struct.make_struct()

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                (w, h), d = imagesize.get(img_fn), 3

                xml_annot = XmlParser()
                xml_annot.set_filename_root(f'{idx}{self.struct.image_ext}')
                xml_annot.set_size_root([h, w, d])

                for annt in annts:
                    xml_annot.add_sub_object(name=annt.label, bbox=annt.bbox)

                # change image name in xml file
                xml_annot.root.find('filename').text = str(idx)+'.jpg'

                # write annot
                xml_annot.write_root(self.struct.get_annotation_file(idx))

                # write image
                shutil.copy(img_fn, self.struct.get_image_file(idx))

                pbar.update(1)

        # make txt list with train/test filenames
        self.create_imagesets(idx)
