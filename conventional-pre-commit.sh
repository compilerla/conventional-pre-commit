#!/usr/bin/env bash

# Define Color Codes
LBLUE='\033[00;34m'
LRED='\033[01;31m'
RESTORE='\033[0m'
YELLOW='\033[00;33m'

# list of Conventional Commits types
cc_types=("feat" "fix")
default_types=("build" "chore" "ci" "docs" "${cc_types[@]}" "perf" "refactor" "revert" "style" "test")
types=( "${cc_types[@]}" )

if [ $# -eq 1 ]; then
    types=( "${default_types[@]}" )
else
    # assume all args but the last are types
    while [ $# -gt 1 ]; do
        types+=( "$1" )
        shift
    done
fi

# the commit message file is the last remaining arg
msg_file="$1"

# join types with | to form regex ORs
r_types="($(IFS='|'; echo "${types[*]}"))"
# optional (scope)
r_scope="(\([[:alnum:] \/-_]+\))?"
# optional breaking change indicator and colon delimiter
r_delim='!?:'
# subject line, body, footer
r_subject=" [[:print:]].+"
# the full regex pattern
pattern="^$r_types$r_scope$r_delim$r_subject$"

# Check if commit is conventional commit
if grep -Eq "$pattern" "$msg_file"; then
    exit 0
fi

echo -e "${LRED}[Bad Commit message] >> ${RESTORE} \"$( cat "$msg_file" )\""
echo -e "${YELLOW}
Your commit message does not follow Conventional Commits formatting
${LBLUE}https://www.conventionalcommits.org/${YELLOW}

Conventional Commits start with one of the below types, followed by a colon,
followed by the commit message:${RESTORE}

    $(IFS=' '; echo "${types[*]}")

${YELLOW}Example commit message adding a feature:${RESTORE}

    feat: implement new API

${YELLOW}Example commit message fixing an issue:${RESTORE}

    fix: remove infinite loop

${YELLOW}Optionally, include a scope in parentheses after the type for more context:${RESTORE}

    fix(account): remove infinite loop
"
exit 1
