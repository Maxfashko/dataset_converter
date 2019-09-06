data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='/tmp/VOCdevkit',
        dir_name='VOC2007'
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='/tmp/VOCdevkit_YOLO',
        dir_name='VOC2007'
    )
)
