#!/usr/bin/env python

import argparse
from dataset_converter.config.config import Config
from dataset_converter.dataset.provider import Provider as dataset_provider
from dataset_converter.data_action.action_processor import ActionProcessor


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='config file path', type=str)

    known_args, unknown_args = parser.parse_known_args()
    return known_args, unknown_args


def main(args=None):
    known_args, unknown_args = parse_args(args)
    cfg = Config.fromfile(known_args.config)

    # parse annotations to standartized format
    parser = dataset_provider.get_dataset(cfg.data.input_data)
    annotations_container = parser.parse()

    # data actions: slice, filter etc...
    if cfg.data.data_actions:
        action_processor = ActionProcessor(cfg.data.data_actions, annotations_container)
        annotations_container = action_processor.process()

    # convert from standartized format to selected type dataset
    converter = dataset_provider.get_dataset(cfg.data.output_data)
    print('converter', converter)
    converter.convert(annotations_container)


if __name__ == '__main__':
    main()
