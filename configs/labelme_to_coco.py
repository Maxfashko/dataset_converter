data = dict(
    input_data=dict(
        type="LabelmeDataset",
        data_root='/DATASET/',
        dir_name='labelme/',
        images='images',
        annotations='xml',
    ),

    output_data=dict(
        type="CocoDataset",
        data_root='/tmp/',
        dir_name='coco',
        params=dict(
            train_test_split=dict(
                train=1,
                test=0,
                seed=42
            )
        )
    )
)
