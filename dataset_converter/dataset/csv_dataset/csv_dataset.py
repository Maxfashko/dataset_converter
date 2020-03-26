import os.path as osp

from tqdm import tqdm
from sklearn.model_selection import train_test_split

from dataset_converter.dataset import CustomDataset
from dataset_converter.dataset import CsvStructDataset


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
            annotations=self.annotations
        )

    @CustomDataset.init_parse
    def parse(self):
        raise NotImplementedError

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
