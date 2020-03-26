import os
import sys
import glob
import shutil
import os.path as osp


class LabelmeStructDataset:
    def __init__(self, **kwargs):
        self.dir_name = kwargs['dir_name']
        self.data_root = kwargs['data_root']
        self.annotations = kwargs['annotations']
        self.scribbles = kwargs['scribbles']
        self.images = kwargs['images']
        self.masks = kwargs['masks']
        self.info = kwargs['info']

        self.annot_ext = '.xml'
        self.image_ext = '.jpg'

        self.info_dir_project = self.check_path(self.info, 'Info')
        self.mask_dir_project = self.check_path(self.masks, 'Masks')
        self.image_dir_project = self.check_path(self.images, 'Images')
        self.annot_dir_project = self.check_path(self.annotations, 'Annotations')
        self.scribbles_dir_project = self.check_path(self.scribbles, 'Scribbles')

    def check_path(self, arg_obj, prefix_dir):
        if arg_obj is None:
            path = osp.join(self.data_root, prefix_dir)
            result_obj = osp.join(path, self.dir_name)
        else:
            result_obj = osp.join(self.data_root, self.dir_name, arg_obj)

        print(result_obj)

        if osp.exists(result_obj):
            return result_obj
        return None

    def check_struct_path(self):
        if not osp.exists(self.data_root):
            return False
        return True

    def check_project_path(self):
        # ограничиваемся минимальным набором: labels, images
        if self.image_dir_project is None:
            print(f'image_dir_project: {self.image_dir_project}')
        if self.annot_dir_project is None:
            print(f'annot_dir_project: {self.annot_dir_project}')
            return False
        return True

    def make_project_path(self, rewrite=True):
        if self.mask_dir_project is not None:
            ret = [osp.exists(x) for x in [self.info_dir_project,
                                           self.mask_dir_project,
                                           self.image_dir_project,
                                           self.annot_dir_project,
                                           self.scribbles_dir_project]]
        else:
            ret = [osp.exists(x) for x in [self.info_dir_project,
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
        print('<<<<1')
        os.makedirs(self.info_dir_project)
        os.makedirs(self.mask_dir_project)
        os.makedirs(self.image_dir_project)
        os.makedirs(self.annot_dir_project)
        os.makedirs(self.scribbles_dir_project)
        print('<<<<2')

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
