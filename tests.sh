#!/usr/bin/env bash

this_dir="$PWD"
test_dir=""
result=0

setup () {
    test_dir=$(mktemp -d)

    cp "$this_dir/.pre-commit-config.yaml" "$test_dir/"
    cp "$this_dir/conventional-pre-commit.sh" "$test_dir/"

    cd "$test_dir"

    git init
    pre-commit install --hook-type commit-msg
    git add .
}

teardown () {
    cd "$this_dir"
    rm -rf "$test_dir"
}

# test a failure

setup

fail="$(git commit -m 'bad: conventional-pre-commit' 2>&1 > /dev/null)"

teardown

echo "$fail" | grep -Eq "Your commit message does not follow Conventional Commits formatting"

(( result += "$?" ))

# test a success

setup

pass="$(git commit -m 'test: conventional-pre-commit')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit"

(( result += "$?" ))

exit "$result"
