data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/tmp/coco/',
        dir_name='head',
        images='images/',
        annotations='annotations/annotation_data.json',
    ),
    output_data = dict(
        type="CocoDataset",
        data_root='/tmp/coco/',
        dir_name='head2',
        params = dict(
            train_test_split=dict(
                train=0.8,
                test=0.2,
                seed=42
            )
        )
    ),
    data_actions = [
        dict(
            type="FilterBBoxAction",
            min_area=20 # pix
        )
    ]
)
