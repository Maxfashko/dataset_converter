data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/mnt/data/data',
        dir_name='coco',
        images='images/val2017',
        annotations='annotations/instances_val2017.json',
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='/tmp/yolo_coco',
        dir_name='val2017',
        params = dict(
            train_test_split=dict(
                train=1,
                test=0,
                seed=42
            )
        )
    )
)
