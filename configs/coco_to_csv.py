data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/home/maksim/data/vizorlabs/DATASETS/',
        dir_name='persons_all_flow',
        images='images/',
        annotations='annotation_data.json',
    ),

    output_data=dict(
        type="CsvDataset",
        data_root='/tmp/',
        dir_name='csv',
        annotations='annotation_data.csv',
        params=dict(
            train_test_split=dict(
                train=0.8,
                test=0.2,
                seed=42
            )
        )
    )
)
