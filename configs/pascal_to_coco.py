data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='/mnt/data/data/head_data/',
        dir_name='combined'
    ),
    output_data = dict(
        type="CocoDataset",
        data_root='/tmp/coco',
        dir_name='head',
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
            type="FilterLabelsAction",
            allowed_labels=[],
            labels_mapping={
                'personw':'head',
                'person':'head'
            }
        ),
        dict(
            type="FilterBBoxAction",
            min_area=20 # pix
        )
    ]
)
