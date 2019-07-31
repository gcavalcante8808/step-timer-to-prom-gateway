SHELL = /bin/bash
.SHELLFLAGS = -euox pipefail -c
.RECIPEPREFIX +=
.PHONY: test test-ci

test:
    coverage run --source=./src -m pytest src/tests/
    coverage html

test-ci: test
    codecov --token=$${CODECOV_TOKEN} --commit=${COMMIT_SHA}

release:
    @echo "Not Implemented Yet."
    exit 1

build_and_test_release_binaries:
    pyinstaller -F step_timer.py
    pyinstaller -F send_to_prometheus_gateway
    dist/step_timer --help
    dist/send_to_prometheus_gateway --help
