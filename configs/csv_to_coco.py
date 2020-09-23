data = dict(
    input_data=dict(
        type="CsvDataset",
        data_root='/tmp/',
        dir_name='scv',
        images='part1/',
        annotations='annot.csv',
    ),

    output_data=dict(
        type="CocoDataset",
        data_root='/tmp/12/',
        dir_name='coco/',
        params=dict(
            train_test_split=dict(
                train=0.8,
                test=0.2,
                seed=42
            )
        )
    ),
)
