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
    input_data = dict(
        type="PascalDataset",
        data_root='/home/maksim/ssd_data/',
        dir_name='combined_15_08_19'
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='/home/maksim/ssd_data/',
        dir_name='combined_15_08_19_yolo'
    )
)
