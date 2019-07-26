import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='./data/pascal',
        dir_name='project1'
    ),

    output_data = dict(
        type="LabelmeDataset",
        data_root='./data/Labelme',
        dir_name='project1'
    )
)
