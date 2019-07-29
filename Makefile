SHELL = /bin/bash
.SHELLFLAGS = -euox pipefail -c
.RECIPEPREFIX +=
.PHONY: test test-ci

test:
    coverage run --source=./src -m pytest src/tests.py
    coverage html

test-ci: test
    codecov --token=$${CODECOV_TOKEN} --commit=${COMMIT_SHA}

