#!/bin/sh

set -e

python setup.py test
python setup.py bdist_egg