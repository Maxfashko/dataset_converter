data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/DATASET/',
        dir_name='coco/',
        images='images/',
        annotations='annotations/annotation_data.json',
    ),

    output_data=dict(
        type="CsvDataset",
        data_root='/tmp/',
        dir_name='scv',
        annotations='annotation_data.json',
        params=dict(
            train_test_split=dict(
                train=0.8,
                test=0.2,
                seed=42
            )
        )
    )
)
