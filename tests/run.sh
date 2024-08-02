#!/usr/bin/env bash
set -eux

# run normal pytests
coverage run -m pytest

# clean out old coverage results
rm -rf ./tests/coverage

# regenerate coverage report
coverage html --directory ./tests/coverage
