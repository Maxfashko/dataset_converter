import os.path as osp

from tqdm import tqdm
from sklearn.model_selection import train_test_split
from glob import glob
import sys
from pathlib import Path
import pandas as pd

from dataset_converter.dataset import CustomDataset
from dataset_converter.dataset import CsvStructDataset
from dataset_converter.parser.container import Annotation, AnnotationsContainer, BBox


class CsvDataset(CustomDataset):
    """
    image, x1,y1,x2,y2,label
    1.jpg,790,164,838,222,person
    """

    def __init__(self, params=None, images=None, annotations=None, **kwargs):
        super(CsvDataset, self).__init__()
        self.data_root = kwargs['data_root']
        self.dir_name = kwargs['dir_name']
        self.annotations = annotations
        self.images = images
        self.params = params

        self.data_path = osp.join(self.data_root, self.dir_name)
        self.struct = CsvStructDataset(
            data_root=self.data_root,
            dir_name=self.dir_name,
            annotations=self.annotations,
            images=self.images
        )

    @CustomDataset.init_parse
    def parse(self):
        # if not self.struct.check_path():
        #     print(f'path not exists! {self.data_path}')
        #     sys.exit()

        annotations_container = AnnotationsContainer()
        annotation_file = Path(self.struct.path, self.struct.annotations)
        if not annotation_file.exists():
            print(f'{self.annotations} is not exists!')
            sys.exit()

        data = pd.read_csv(annotation_file)

        unique_filenames = data["image"].unique()

        with tqdm(total=len(unique_filenames)) as pbar:
            for unique_filename in unique_filenames:
                annotations = []
                # basename, _ = unique_filename

                df = data[data["image"] == unique_filename]
                for index, row in df.iterrows():
                    annotations.append(
                        Annotation(
                            bbox=BBox(x1=row["x1"], y1=row["y1"], x2=row["x2"], y2=row["y2"]),
                            label=row["label"]
                        )
                    )

                annotations_container.add_data(
                    annotations=annotations,
                    image_filename=str(Path(self.struct.path, self.struct.images + Path(unique_filename).name)),
                    annotation_filename=None
                )
                pbar.update(1)
            return annotations_container

    def train_val_split(self, test_size, seed):

        df = self.struct.data_to_df()

        train, val = train_test_split(df, test_size=test_size, random_state=seed)

        print('train images', len(train))
        print('val images', len(val))

        # dump files
        all_fn = osp.join(self.struct.path, 'annotation_data' + self.struct.annot_ext)
        train_fn = osp.join(self.struct.path, 'train' + self.struct.annot_ext)
        val_fn = osp.join(self.struct.path, 'val' + self.struct.annot_ext)

        print('dump annotations to', train_fn, val_fn)

        self.struct.dump(train, train_fn)
        self.struct.dump(val, val_fn)
        self.struct.dump(df, all_fn)

    @CustomDataset.init_convert
    def convert(self, annotations_container):
        # create structure over drive
        self.struct.make_struct()

        with tqdm(total=annotations_container.get_len()) as pbar:
            for idx, annts, img_fn, annt_fn in annotations_container.get_data():
                for annt in annts:
                    self.struct.add_data(img_fn, annt.bbox, annt.label)
                pbar.update(1)

        # make train val/json files
        test_size, seed = None, None
        try:
            test_size = self.params.get('train_test_split').get('test')
            seed = self.params.get('train_test_split').get('seed')
        except Exception as e:
            pass

        if test_size and seed:
            self.train_val_split(test_size, seed)
        else:
            all_fn = osp.join(self.struct.path, 'annotation_data' + self.struct.annot_ext)
            self.struct.dump(self.struct.data_to_df(), all_fn)
