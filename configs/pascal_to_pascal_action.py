import os.path as osp

data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project1'
    ),

    output_data = dict(
        type="PascalDataset",
        data_root='data',
        dir_name='project1_crop
    ),


    data_actions = [
        dict(
            type="RandomCropAction",

            # the number of random crops from the original image
            n_crops=5,

            # Filter bounding boxes and return only those boxes whose visibility after transformation is above
            # the threshold and minimal area of bounding box in pixels is more then min_area.
            min_area=100,

            # the number of iterations that the action should do until it reaches the value of <n_crops>
            max_iters=50,
            width=1920,
            height=1080

        ),
        # not implemented!
        # dict(
        #     type="FilterLabel",
        #     label_mapping={
        #         'pedestrian':'person',
        #         'man':'person'
        #     }
        # )
    ]
)
