import shutil
from glob import glob
import os.path as osp
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import imagesize
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from utils.dataset.custom_dataset import CustomDataset
from utils.dataset.pascal_dataset.xmlparser import XmlParser
from utils.parser.container import Container, Containers, BBox
from utils.dataset.pascal_dataset.pascal_struct_dataset import PascalStructDataset


class PascalDataset(CustomDataset):
    def __init__(self, data_path):
        super(CustomDataset, self).__init__()
        self.struct = PascalStructDataset(path=data_path)
        self.counter = 0

    def parse(self):
        print('parse')

        containers = Containers()
        filenames = list(glob(f'{self.struct.annot_dir}/*{self.struct.annot_ext}'))[:100]

        with tqdm(total=len(filenames)) as pbar:
            for fn in filenames:
                basename, _ = osp.splitext(osp.basename(fn))

                tree = ElementTree.parse(fn)
                root = tree.getroot()

                for obj in root.findall('object'):
                    bbox = obj.find('bndbox')

                    container = Container(
                        bbox=BBox(
                            x1=int(bbox.find("xmin").text),
                            y1=int(bbox.find("ymin").text),
                            x2=int(bbox.find("xmax").text),
                            y2=int(bbox.find("ymax").text)),
                        label=obj.find("name").text
                    )

                    containers.add(name=basename, val=container)
                pbar.update(1)
        return containers

    def create_imagesets(self, idx, test_size=0.2, seed=42):
        ''' create ImageSets train/val '''

        try:
            numbers = [x for x in range(0, idx)]
            train, test, _, _ = train_test_split(numbers, numbers, test_size=test_size, random_state=seed)

            self.struct.make_image_list(train, 'train')
            self.struct.make_image_list(test, 'test')
        except Exception as e:
            raise

    def convert(self, containers, containers_struct):
        print('convert')

        # create structure over drive
        if not self.struct.check_path():
            self.struct.make_struct()

        with tqdm(total=len(list(containers.containers))) as pbar:
            for idx, (filename, containers) in enumerate(containers.containers):
                filename_img = containers_struct.get_image_file(filename)
                (w, h), d = imagesize.get(filename_img), 3

                xml_annot = XmlParser()
                xml_annot.set_filename_root(f'{idx}{containers_struct.image_ext}')
                xml_annot.set_size_root([h, w, d])

                for container in containers:
                    xml_annot.add_sub_object(name=container.label, bbox=container.bbox)

                # change image name in xml file
                xml_annot.root.find('filename').text = str(idx)+'.jpg'

                # write annot
                xml_annot.write_root(self.struct.get_annotation_file(idx))

                # write image
                shutil.copy(filename_img, self.struct.get_image_file(idx))
                pbar.update(1)

        # make txt list with train/test filanames
        self.create_imagesets(idx)
