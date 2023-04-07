#!/bin/bash

python3 -m pip install -U wheel twine setuptools
python3 ./django_moncash/setup.py sdist
python3 ./django_moncash/setup.py bdist_wheel
twine upload ./django_moncash/dist/*