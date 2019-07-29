SHELL = /bin/bash
.SHELLFLAGS = -euox pipefail -c
.RECIPEPREFIX +=

test:
    coverage run --source=./src -m pytest src/tests.py
    coverage html
