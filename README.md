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

**parse** - the method provides an opportunity to read data and convert it into a unified structure, which operates with all dataset formats

**convert** - the method provides the ability to convert data from a unified structure into the selected dataset format

**convert** - support for data that can be set as paths to the annotation directory and images


## Installation

`python setup.py install`

## Get Started

### convert dataset
In this example, we download and convert data from the PASCAL format to the YOLO format.

1) Download dataset PASCAL_VOC 2007:

```shell
cd /tmp
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
tar xvf VOCtrainval_06-Nov-2007.tar
```


2) The parameters for data conversion are located in the configuration file (https://github.com/Maxfashko/dataset_converter/blob/master/configs/pascal_to_yolo.py) replace the `data_root`, `dir_name` options. As a result, the configuration file should look like this:

```python
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
```


3) To convert your dataset from the PASCAL format to the YOLO format, use the following command:

```shell
python tools/convert.py configs/pascal_to_yolo.py
```

you will see the following output:

```shell
start parse...
100%|████████████████████████████████████████████████████████████████████████████████████████████| 5011/5011 [00:00<00:00, 30432.46it/s]
parse completed
start convert...
classes: {'sheep': 0, 'bus': 1, 'chair': 2, 'tvmonitor': 3, 'boat': 4, 'cat': 5, 'pottedplant': 6, 'train': 7, 'dog': 8, 'bottle': 9, 'bicycle': 10, 'person': 11, 'horse': 12, 'car': 13, 'aeroplane': 14, 'diningtable': 15, 'sofa': 16, 'bird': 17, 'cow': 18, 'motorbike': 19}
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 5011/5011 [00:00<00:00, 15454.61it/s]
convert completed
```


4) By default, the data is split for training and testing in the proportion of 80/20. You can specify your values:

```python
data = dict(
    input_data = dict(
        type="PascalDataset",
        data_root='/tmp/VOCdevkit',
        dir_name='VOC2007'
    ),

    output_data = dict(
        type="YoloDataset",
        data_root='/tmp/VOCdevkit_YOLO',
        dir_name='VOC2007',
        params = dict(
            train_test_split=dict(
                train=0.9,
                test=0.1,
                seed=42
            )
        )
    )
)
```
