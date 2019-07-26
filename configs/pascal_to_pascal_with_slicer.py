import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='/mnt/data/data/avaks/tatka',
        dir_name='2+3+4+6_combined/'
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='/mnt/data/data/avaks/tatka',
        dir_name='2+3+4+6_combined_slice/'
    ),

    data_actions = [
        dict(
            type="ImageSlicer",
            tile_size=(1080, 1920),
            tile_step=(1000, 1800)
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
