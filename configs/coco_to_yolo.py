# data = dict(
#     input_data = dict(
#         type="PascalDataset",
#         data_root='data',
#         dir_name='project1'
#     ),
#
#     output_data = dict(
#         type="YoloDataset",
#         data_root='/tmp',
#         dir_name='project1'
#     )
# )

data = dict(
    input_data=dict(
        type="CocoDataset",
        data_root='/mnt/data/data',
        dir_name='coco',
        images='images/val2017',
        annotations='annotations/instances_val2017.json',
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='/home/maksim/ssd_data',
        dir_name='combined_15_08_19_yolo+coco',
        params = dict(
            train_test_split=dict(
                train=1,
                test=0,
                seed=42
            )
        )
    ),

    data_actions = [
        dict(
            type="FilterLabelsAction",
            allowed_labels=[
                'person'
            ]
            # label_mapping={
            #     'pedestrian':'person',
            #     'man':'person'
            # }
        )
    ]
)
