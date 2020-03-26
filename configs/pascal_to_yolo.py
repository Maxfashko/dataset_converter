data = dict(
    input_data=dict(
        type="PascalDataset",
        data_root='/DATASET/',
        dir_name='pascal'
    ),

    output_data=dict(
        type="YoloDataset",
        data_root='/tmp/',
        dir_name='yolo'
    )
)
