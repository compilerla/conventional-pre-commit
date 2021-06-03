#!/usr/bin/env bash

if ! grep -Pq '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([\w][\w -]+\))?!?: [\w][\s\S]+$' "$1"; then
    echo "[Commit message] $( cat $1 )"
    echo "
Your commit message doesn't look like a Conventional Commit https://www.conventionalcommits.org/

Conventional Commits start with one of the below types, followed by a colon, followed by the commit message:

    build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test

Example commit message adding a feature:

    'feat: add great new feature'

Example commit message fixing an issue:

    'fix: remove infinite loop'

Optionally, include a scope in parentheses after the type for more context:

    'fix(account): remove infinite loop'
"
    exit 1
fi