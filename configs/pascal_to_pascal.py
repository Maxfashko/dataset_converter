import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project1'
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='/tmp',
        dir_name='project1'
    )
)
