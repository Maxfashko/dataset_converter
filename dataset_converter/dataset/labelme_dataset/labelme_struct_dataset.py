import os
import sys
import glob
import shutil
import os.path as osp


class LabelmeStructDataset:
    def __init__(self, **kwargs):
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.images = kwargs['images']
        self.annotations = kwargs['annotations']

        self.annot_ext = '.xml'
        self.image_ext = '.jpg'

        self.info_dir = osp.join(self.data_root, 'Info')
        self.mask_dir = osp.join(self.data_root, 'Masks')

        if not self.images:
            self.image_dir = osp.join(self.data_root, 'Images')
        else:
            print('data that does not match the structure of the dataset is NotImplemented for LabelmeStructDataset')
            sys.exit(-1)

        if not self.annotations:
            self.annot_dir = osp.join(self.data_root, 'Annotations')
        else:
            print('data that does not match the structure of the dataset is NotImplemented for LabelmeStructDataset')
            sys.exit(-1)

        self.scribbles_dir = osp.join(self.data_root, 'Scribbles')

        self.info_dir_project = osp.join(self.info_dir, self.dir_name)
        self.mask_dir_project = osp.join(self.mask_dir, self.dir_name)
        self.image_dir_project = osp.join(self.image_dir, self.dir_name)
        self.annot_dir_project = osp.join(self.annot_dir, self.dir_name)
        self.scribbles_dir_project = osp.join(self.scribbles_dir, self.dir_name)

    def check_struct_path(self):
        if not osp.exists(self.data_root):
            return False
        return True

    def check_project_path(self):
        ret = [osp.exists(x) for x in [self.image_dir_project,
                                       self.mask_dir_project,
                                       self.info_dir_project]]
        if False in ret:
            return False
        return True

    def make_project_path(self, rewrite=True):
        ret = [osp.exists(x) for x in [ self.info_dir_project,
                                        self.mask_dir_project,
                                        self.image_dir_project,
                                        self.annot_dir_project,
                                        self.scribbles_dir_project]]
        if True in ret:
            if not rewrite:
                print('directory already exists!')
                sys.exit(-1)
            else:
                for p in [self.info_dir_project,
                          self.mask_dir_project,
                          self.image_dir_project,
                          self.annot_dir_project,
                          self.scribbles_dir_project]:
                    try:
                        shutil.rmtree(p)
                    except Exception as e:
                        pass

        os.makedirs(self.info_dir_project)
        os.makedirs(self.mask_dir_project)
        os.makedirs(self.image_dir_project)
        os.makedirs(self.annot_dir_project)
        os.makedirs(self.scribbles_dir_project)

    def make_struct_path(self, rewrite=False):
        if self.check_struct_path():
            if not rewrite:
                print('directory already exists!')
                sys.exit(-1)
            else:
                shutil.rmtree(self.data_root)

        os.makedirs(self.data_root)
        os.makedirs(self.annot_dir)
        os.makedirs(self.image_dir)
        os.makedirs(self.mask_dir)
        os.makedirs(self.info_dir)
        os.makedirs(self.scribbles_dir)

    def get_annotation_file(self, idx):
        return os.path.join(self.annot_dir_project, f'{idx}{self.annot_ext}')

    def get_image_file(self, idx):
        return os.path.join(self.image_dir_project, f'{idx}{self.image_ext}')
