import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project1'
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project2'
    ),

    data_actions = [
        dict(
            type="ImageSlicer",
            tile_size=(1080, 1920),
            tile_step=(512, 512)
        ),
        # not implemented!
        # dict(
        #     type="FilterLabel",
        #     label_mapping={
        #         'pedestrian':'person',
        #         'man':'person'
        #     }
        # )
    ]
)
