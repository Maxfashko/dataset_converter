import setuptools
from setuptools.extension import Extension
import numpy as np

setuptools.setup(
    name             = 'dataset_converter',
    version          = '0.1.0',
    description      = 'A tool to convert annotation from one type to other types.',
    url              = 'https://github.com/Maxfashko/dataset_converter',
    author           = 'Maksim Koriukin',
    author_email     = 'maxfashko@gmail.com',
    maintainer       = 'Maksim Koriukin',
    maintainer_email = 'maxfashko@gmail.com',
    packages         = ['dataset_converter'],
    install_requires = ['tqdm', 'addict', 'opencv-python'],
    classifiers=[
        'Development Status :: 0.1.0 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)
