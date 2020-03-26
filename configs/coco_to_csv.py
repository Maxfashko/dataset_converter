data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/DATASETS/',
        dir_name='coco/',
        images='images/',
        annotations='annotations/annotation_data.json',
    ),

    output_data=dict(
        type="CsvDataset",
        data_root='/tmp/',
        dir_name='csv',
        annotations='annotation_data.csv'
    )
)
