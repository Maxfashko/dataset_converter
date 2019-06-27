#!/usr/bin/env python

import argparse
from utils.config.config import Config
from utils.dataset.filter import Filter
from utils.dataset.provider import Provider


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='config file path', type=str)

    known_args, unknown_args = parser.parse_known_args()
    return known_args, unknown_args


def main(args=None):
    known_args, unknown_args = parse_args(args)
    cfg = Config.fromfile(known_args.config)

    # parse annotations to standartized format
    parser = Provider.get_dataset(cfg.data.input_data)
    annotations_container = parser.parse()

    # filter annotation if necessary
    if cfg.filter_params.filtration:
        flt = Filter(
            cfg=cfg.filter_params,
            annotations_container=annotations_container
        )

        annotations_container = flt.filter_out()

    # convert from standartized format to selected type dataset
    converter = Provider.get_dataset(cfg.data.output_data)
    converter.convert(annotations_container)


if __name__ == '__main__':
    main()
