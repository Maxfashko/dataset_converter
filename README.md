## Introduction

dataset converter is a toolkit for converting object detection datasets. Designed to easily convert your data into popular dataset formats.


## Allowed dataset types

Supported methods are shown in the below table

|                    | parse  | convert | unstructured support |
|--------------------|:------:|:-------:|:--------------------:|
| COCO               | ✓      | ✗       | ✗                    |
| PASCAL             | ✓      | ✓       | ✓                    |
| Labelme-web        | ✓      | ✓       | ✗                    |
| YOLO               | ✗      | ✓       | ✓                    |


## Installation

`python setup.py install`

## Get Started

### convert dataset

To convert your dataset from the PASCAL format to the YOLO format, use the following command:

```shell
python tools/convert.py configs/pascal_to_yolo.py
```

The parameters for data conversion are located in the configuration file:

```shell
configs/pascal_to_yolo.py
```

```python
data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='./data/VOCdevkit',
        dir_name='VOC2007'
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='./data/VOCdevkit_YOLO',
        dir_name='VOC2007'
    )
)
```
