import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='/home/pascal_format',
        dir_name='project1'
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='/tmp',
        dir_name='2'
    ),

    filter_params = dict(
        filtration = True,
        labels_params=dict(
            allowed_labels=['person']
        )
    )
)
