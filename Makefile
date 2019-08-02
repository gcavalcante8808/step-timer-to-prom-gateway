SHELL = /bin/bash
.SHELLFLAGS = -euox pipefail -c
.RECIPEPREFIX +=
.PHONY: test test-ci

test:
    coverage run --source=./src -m pytest src/tests/
    coverage html

test-ci: test
    codecov --token=$${CODECOV_TOKEN} --commit=${COMMIT_SHA}

release: clear build_and_test_release_binaries
    cd src
    ghr -replace v1.0.0 dist/


.ONESHELL: build_and_test_release_binaries
build_and_test_release_binaries:
    cd src
    pyinstaller -F step_timer.py
    pyinstaller -F send_to_prometheus_gateway.py
    dist/step_timer --help
    dist/send_to_prometheus_gateway --help

clear:
    cd src
    rm -rf dist/ rm -rf build/
