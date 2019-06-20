#!/usr/bin/env python

import argparse
from utils.config.config import Config
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
    containers = parser.parse()

    # convert from standartized format to selected type
    converter = Provider.get_dataset(cfg.data.output_data)
    converter.convert(containers=containers, containers_struct=parser.struct)


if __name__ == '__main__':
    main()
