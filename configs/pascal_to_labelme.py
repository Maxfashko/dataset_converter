import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project1'
    ),

    output_data = dict(
        type="LabelmeDataset",
        data_root='/tmp/Labelme_annotations',
        dir_name='project1',
        labels_params=dict(
            allowed_labels=['person']
        )
    ),

    filter_params = dict(
        filtration = True,
        labels_params=dict(
            allowed_labels=['person']
        )
    )
)
