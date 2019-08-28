import os
import sys
import glob
import shutil
import os.path as osp


class YoloStructDataset:
    def __init__(self, path, images, annotations):
        self.path = path
        self.images = images
        self.annotations = annotations

        self.annot_ext = '.txt'
        self.image_ext = '.jpg'
        self.test_list_name = 'test.txt'
        self.train_list_name = 'train.txt'

        if not self.annotations:
            self.annot_dir = self.path
        else:
            self.annot_dir = os.path.join(self.path, self.annotations)

        if not self.images:
            self.image_dir = self.path
        else:
            self.image_dir = os.path.join(self.path, self.images)

        self.image_sets = self.path + '/ImageSets/'

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
        os.makedirs(self.image_sets)

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
        return os.path.join(self.image_sets, self.test_list_name)

    def get_train_file(self):
        return os.path.join(self.image_sets, self.train_list_name)

    def get_annotation_file(self, fn):
        return os.path.join(self.annot_dir, f'{fn}{self.annot_ext}')

    def get_image_file(self, fn):
        return os.path.join(self.image_dir, f'{fn}{self.image_ext}')

    def get_annotation_files(self):
        return glob.glob(osp.join(self.annot_dir, f'*{self.annot_ext}'))

    def get_image_files(self):
        return glob.glob(osp.join(self.image_dir, f'*{self.image_ext}'))
