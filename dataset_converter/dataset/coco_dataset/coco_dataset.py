import sys
import json
import shutil
from glob import glob
import os.path as osp

import imagesize
from tqdm import tqdm
from pycocotools.coco import COCO
from sklearn.model_selection import train_test_split

from dataset_converter.dataset.custom_dataset import CustomDataset
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox
from dataset_converter.dataset.coco_dataset.coco_struct_dataset import CocoStructDataset


class CocoDataset(CustomDataset):
    def __init__(self, params=None, images=None, annotations=None, **kwargs):
        super(CustomDataset, self).__init__()
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.images = images
        self.params = params
        self.annotations = annotations

        self.data_path = osp.join(self.data_root, self.dir_name)
        self.params = params
        self.struct = CocoStructDataset(
            path=self.data_path,
            images=self.images,
            annotations=self.annotations)

    @CustomDataset.init_parse
    def parse(self):
        if not self.struct.check_path():
            print(f'path not exists! {self.data_path}')
            sys.exit()

        annotations_container = AnnotationsContainer()

        with tqdm(total=len(self.struct)) as pbar:
            for annt_ids, img_id in self.struct.provider():
                annotations = []

                for annt_id in annt_ids:
                    annotations.append(
                        Annotation(
                            bbox=self.struct.get_bbox(annt_id),
                            label=self.struct.get_label(annt_id)
                        )
                    )

                annotations_container.add_data(
                    annotations=annotations,
                    image_filename=self.struct.get_image_name(img_id),
                    annotation_filename=None
                )
                pbar.update(1)
        return annotations_container

    def train_val_split(self, datapath, train, test, seed):
        coco = COCO(datapath)

        with open(datapath) as f:
            data = json.load(f)

        image_idx = [x['id'] for x in data['images']]
        train_img_idx, val_img_idx, _, _ = train_test_split(image_idx, image_idx, test_size=test, random_state=seed)

        train = {'images': [], "annotations": [], 'categories': [], "licenses": data['licenses']}
        val = {'images': [], "annotations": [], 'categories': [], "licenses": data['licenses']}

        for annot in data['annotations']:
            if self.struct.is_val(annot['image_id'], val_img_idx):
                val['annotations'].append(annot)
            else:
                train['annotations'].append(annot)

        self.struct.added_images(train, coco)
        self.struct.added_images(val, coco)

        self.struct.added_categories(train, coco)
        self.struct.added_categories(val, coco)

        # self.struct.added_segmentation(train, coco)
        # self.struct.added_segmentation(val, coco)

        print('train images', len(train['images']))
        print('val images', len(val['images']))
        print('train annot:', len(train['annotations']))
        print('val annot:', len(val['annotations']))

        # dump files
        train_fn = osp.join(self.struct.annot_dir, 'train.json')
        val_fn = osp.join(self.struct.annot_dir, 'val.json')

        print('dump annotations to', train_fn, val_fn)

        self.struct.dump_data(train, train_fn)
        self.struct.dump_data(val, val_fn)

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        self.struct.make_struct()

        categories_dict = annotations_container.mapping_labels_to_int()

        # append categories
        for k, v in categories_dict.items():
            self.struct.add_category(name=k, id=v)

        annotation_id = 0

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():

                try:
                    (w, h) = imagesize.get(img_fn)
                except Exception as e:
                    print(e)
                    continue

                # write image
                shutil.copy(img_fn, self.struct.get_image_file(idx))

                # append image
                self.struct.add_image(
                    filename=osp.join(str(idx) + self.struct.image_ext),
                    height=h,
                    width=w,
                    id=idx)

                for annt in annts:
                    self.struct.add_annot(
                        bbox=annt.bbox,
                        image_id=idx,
                        category_id=categories_dict[annt.label],
                        id=annotation_id)
                    annotation_id += 1

                pbar.update(1)

        # dump data
        filename = osp.join(self.struct.annot_dir, 'annotation_data.json')
        print('dump annotations to', filename)
        self.struct.dump_data(self.struct.data, filename)

        # make train val/json files
        test = self.params.get('train_test_split').get('test')
        train = self.params.get('train_test_split').get('train')
        seed = self.params.get('train_test_split').get('seed')

        if train and test and seed:
            self.train_val_split(filename, train, test, seed)
