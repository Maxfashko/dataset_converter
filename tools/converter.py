#!/usr/bin/env python

import argparse
from utils.config.config import Config
from utils.provider import Provider

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='config file path', type=str)

    known_args, unknown_args = parser.parse_known_args()
    return known_args, unknown_args


def main(args=None):
    known_args, unknown_args = parse_args(args)
    cfg = Config.fromfile(known_args.config)

    dataset = Provider.get_dataset(cfg.data)
    # data = dataset.parse()
    # dataset.convert(data)


if __name__ == '__main__':
    main()
