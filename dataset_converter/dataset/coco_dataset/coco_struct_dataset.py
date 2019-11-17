import os
import sys
import glob
import json
import shutil
import datetime
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

        try:
            self.dataset = COCO(osp.join(self.path, self.annotations))
            self.provider()
        except Exception as e:
            pass

        self.data = {
            "info": {
                "description": "MyDataset",
                "url": "",
                "version": "1.0",
                "year": str(datetime.datetime.now().year),
                "contributor": "",
                "date_created": str(datetime.datetime.now())
            },
            'images':[],
            "annotations":[],
            'categories':[],
            "licenses":[
                {
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                    "id": 1,
                    "name": "Attribution-NonCommercial-ShareAlike License"
                }
            ]}

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

    def add_image(self, filename, height, width, id, license=1, data_captured="2013-11-14 17:02:52"):
        try:
            data = {
                "license": license,
                "file_name": str(filename),
                "coco_url": str(filename),
                "height": int(height),
                "width": int(width),
                "date_captured": data_captured,
                "flickr_url": str(filename),
                "id": int(id)}
            self.data['images'].append(data)
        except Exception as e:
            raise

    def add_annot(self, bbox, image_id, category_id, id, iscrowd=0):
        try:
            data = {
                "segmentation": [],
                "area": bbox.height * bbox.width,
                "iscrowd": int(iscrowd),
                "image_id": int(image_id),
                "bbox": [
                    bbox.x1,
                    bbox.y1,
                    bbox.width,
                    bbox.height
                ],
                "category_id": int(category_id),
                "id": int(id)}
            self.data['annotations'].append(data)
        except Exception as e:
            raise

    def add_category(self, name, id, supercategory=None):
        try:
            if supercategory is None:
                supercategory = name
            data = {
                "supercategory": str(supercategory),
                "id": int(id),
                "name": str(name)
            }
            self.data['categories'].append(data)
        except Exception as e:
            raise

    def dump_data(self, data, filename):
        with open(osp.join(self.annot_dir, filename), 'w') as f:
            json.dump(data, f)

    def search_by_img_id(self, id, images):
        for img in images:
            if img['id'] == id:
                return img
        return None

    def search_by_cat_id(self, id, categories):
        for cat in categories:
            if cat['id'] == id:
                return cat
        return None

    def get_name_cat(self, id, data):
        for cat in data['categories']:
            if cat['id'] == id:
                return cat['name']
        return None

    def is_val(self, image_id, val_parts):
        for val_id in val_parts:
            if val_id == image_id:
                return True
        return False

    def added_images(self, part, coco):
        images_id = []

        for annot in part['annotations']:
            images_id.append(annot['image_id'])

        images_id = set(images_id)

        for img_id in images_id:
            img = coco.loadImgs(img_id)[0]
            if img:
                part['images'].append(img)

    def added_categories(self, part, coco):
        categories_id = []

        for annot in part['annotations']:
            categories_id.append(annot['category_id'])

        categories_id = set(categories_id)

        for cat_id in categories_id:
            cat = coco.loadCats(cat_id)[0]
            if cat:
                part['categories'].append(cat)

    def added_segmentation(self, part, coco):
        for annot in tqdm(part['annotations']):
            img_obj = coco.loadImgs(annot['image_id'])[0]
            img = np.zeros([img_obj['height'], img_obj['width']], dtype=np.uint8)

            x1 = int(annot['bbox'][0])
            y1 = int(annot['bbox'][1])
            w = int(annot['bbox'][2])
            h = int(annot['bbox'][3])
            x2 = x1 + w
            y2 = y1 + h

            img[y1:y2, x1:x2] = 1
            contours = measure.find_contours(img, 0.5)

            for contour in contours:
                contour = np.flip(contour, axis=1)
                segmentation = contour.ravel().tolist()
                annot["segmentation"].append(segmentation)
