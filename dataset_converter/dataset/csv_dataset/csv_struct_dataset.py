import os
import sys
import glob
import shutil
import os.path as osp

import pandas as pd


class CsvStructDataset:
    def __init__(self, **kwargs):
        self.dir_name = kwargs['dir_name']
        self.data_root = kwargs['data_root']
        self.annotations = kwargs['annotations']
        self.path = osp.join(self.data_root, self.dir_name)
        self.annot_ext = '.json'

        self.data = {'image': [], 'x1': [], 'y1': [], 'x2': [], 'y2': [], 'label': []}

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

    def add_data(self, img_path, bbox, label):
        self.data['image'].append(img_path)
        self.data['x1'].append(bbox.x1)
        self.data['y1'].append(bbox.y1)
        self.data['x2'].append(bbox.x2)
        self.data['y2'].append(bbox.y2)
        self.data['label'].append(label)

    def data_to_df(self):
        return pd.DataFrame.from_dict(self.data)

    def dump(self, data, path):
        save_path = osp.join(self.path, self.annotations)
        data.to_csv(path, index=None, header=False)
