data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/mnt/data/code/object_detection/ml_train/kola/annotation_data/',
        dir_name='coco_struct',
        images='images/train/',
        annotations='annotations/train.json',
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='/tmp/pascal_coco',
        dir_name='KOLAES',
        params = dict(
            train_test_split=dict(
                train=0.8,
                test=0.2,
                seed=42
            )
        )
    )
)
