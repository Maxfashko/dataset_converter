data = dict(
    input_data=dict(
        type="LabelmeDataset",
        data_root='/DATASET/',
        dir_name='labelme'
    ),

    output_data=dict(
        type="PascalDataset",
        data_root='/tmp/',
        dir_name='pascal'
    )
)
