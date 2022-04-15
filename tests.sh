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

    git branch -m main
    git config user.email "conventional-pre-commit@compiler.la"
    git config user.name "conventional-pre-commit"

    pre-commit install --hook-type commit-msg
    git add .
}

teardown () {
    cd "$this_dir"
    rm -rf "$test_dir"
}

echo "test a failure"

setup

fail="$(git commit -m 'bad: conventional-pre-commit' 2>&1 > /dev/null)"

teardown

echo "$fail" | grep -Eq "Your commit message does not follow Conventional Commits formatting"

(( result += "$?" ))

echo "$result"

echo "test a success"

setup

pass="$(git commit -m 'test: conventional-pre-commit')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit"

(( result += "$?" ))

echo "$result"

echo "test printable characters/marks in subject"

echo "test escaped double quote \""

setup

pass="$(git commit -m 'test: conventional-pre-commit "')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit \""

(( result += "$?" ))

echo "$result"

echo "test backtick \`"

setup

pass="$(git commit -m 'test: conventional-pre-commit `')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit \`"

(( result += "$?" ))

echo "$result"

echo "test hash/number sign #"

setup

pass="$(git commit -m 'test: conventional-pre-commit #')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit #"

(( result += "$?" ))

echo "$result"

echo "test ampersand &"

setup

pass="$(git commit -m 'test: conventional-pre-commit &')"

teardown

echo "$pass" | grep -Eq "\[main \(root-commit\) [[:alnum:]]{7}\] test: conventional-pre-commit &"

(( result += "$?" ))

echo "$result"

exit "$result"
