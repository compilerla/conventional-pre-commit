
#!/usr/bin/env bash
set -eux

pytest --cov=conventional_pre_commit --cov-branch --import-mode=importlib

# clean out old coverage results
rm -rf coverage
coverage html --directory coverage
