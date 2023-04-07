#!/bin/bash

cd django_moncash/

python3 -m pip install -U wheel twine setuptools
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*