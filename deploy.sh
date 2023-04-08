#!/bin/bash

rm -r build
rm -r dist
rm -r django_moncash.egg-info

python3 -m pip install -U wheel twine setuptools
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*