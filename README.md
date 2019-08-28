## Introduction

dataset converter is a toolkit for converting object detection datasets.

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

1. Convert PASCAL_VOC to YOLO.

```shell
python tools/convert.py configs/pascal_to_yolo.py
```
