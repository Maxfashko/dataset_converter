data = dict(
    input_data=dict(
        type="CsvDataset",
        data_root='/home/maksim/Документы/TASK/evraz_conveyor/VIDEOARHIV/2020-09-15-part1/',
        dir_name='part1_images_correct',
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
