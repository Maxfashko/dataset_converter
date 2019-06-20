import os.path as osp

data_input_path='/tmp/1'
data_output_path='/tmp/2'

data = dict(
    input_data = dict(
        type="PascalDataset",
        images=osp.join(data_input_path, 'JPEGImages'),
        annotations=osp.join(data_input_path, 'Annotations')
    ),

    output_data = dict(
        type="PascalDataset"
    )
)
