import os
import sys
import glob
import shutil
import os.path as osp

from pycocotools.coco import COCO

from dataset_converter.parser.container import BBox


class CocoStructDataset:
    def __init__(self, path, images, annotations):
        self.path = path
        self.images = images
        self.annotations = annotations

        self.annot_ext = '.json'
        self.image_ext = '.jpg'
        self.test_list_name = 'val' + self.image_ext
        self.train_list_name = 'train' + self.annot_ext
        self.annot_dir = os.path.join(self.path, 'annotations')
        self.image_dir = os.path.join(self.path, 'images')

        self.dataset = COCO(osp.join(self.path, self.annotations))
        self.provider()

    def __len__(self):
        return len(self.dataset.imgs)

    def provider(self):
        for img_id in self.dataset.imgs:
            annt_ids = self.dataset.getAnnIds(img_id)
            yield annt_ids, img_id

    def get_image_size(self, img_id):
        img_info = self.dataset.loadImgs(img_id)[0]
        return img_info['height'], img_info['width']

    def get_image_name(self, img_id):
        img_info = self.dataset.loadImgs(img_id)[0]
        return osp.join(self.path, self.images, img_info['file_name'])

    def get_bbox(self, annt_id):
         annt = self.dataset.loadAnns(annt_id)
         bbox = annt[0]['bbox']
         return BBox(
            x1=bbox[0], y1=bbox[1], x2=bbox[0] + bbox[2], y2=bbox[1] + bbox[3])

    def get_label(self, annt_id):
         annt = self.dataset.loadAnns(annt_id)
         return self.dataset.loadCats(annt[0]['category_id'])[0]['name']



    def check_path(self):
        if os.path.exists(self.path):
            return True
        return False

    def make_struct(self, rewrite=True):
        if self.check_path():
            if not rewrite:
                print('directory already exists!')
                sys.exit(-1)
            else:
                shutil.rmtree(self.path)

        os.makedirs(self.path)
        os.makedirs(self.annot_dir)
        os.makedirs(self.image_dir)

    def make_image_list(self, namelist, mode):
        def f(file, my_list):
            for item in my_list:
                file.write("%s\n" % item)

        if mode == 'train':
            with open(self.get_image_set_train(), 'w') as fh:
                f(fh, namelist)

        if mode == 'test':
            with open(self.get_image_set_test(), 'w') as fh:
                f(fh, namelist)

    def get_train_files(self):
        result = []
        with open(self.get_image_set_train(), 'r') as fh:
            for line in fh:
                result.append(int(line.strip()))
        return result

    def get_test_files(self):
        result = []
        with open(self.get_image_set_test(), 'r') as fh:
            for line in fh:
                result.append(int(line.strip()))
        return result

    def get_image_set_train(self):
        return os.path.join(self.image_sets, self.train_list_name)

    def get_image_set_test(self):
        return os.path.join(self.image_sets, self.test_list_name)

    def get_test_file(self):
        return os.path.join(self.image_sets, 'test.txt')

    def get_train_file(self):
        return os.path.join(self.image_sets, 'trainval.txt')

    def get_annotation_file(self, fn):
        return os.path.join(self.annot_dir, f'{fn}{self.annot_ext}')

    def get_image_file(self, fn):
        return os.path.join(self.image_dir, f'{fn}{self.image_ext}')

    def get_annotation_files(self):
        return glob.glob(
            osp.join(self.annot_dir, f'*{self.annot_ext}'))

    def get_image_files(self):
        return glob.glob(
            osp.join(self.image_dir, f'*{self.image_ext}'))
