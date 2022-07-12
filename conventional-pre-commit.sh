#!/usr/bin/env bash

# Define Color Codes
RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
YELLOW='\033[00;33m'
BLUE='\033[00;34m'
PURPLE='\033[00;35m'
CYAN='\033[00;36m'
LIGHTGRAY='\033[00;37m'

LRED='\033[01;31m'
LGREEN='\033[01;32m'
LYELLOW='\033[01;33m'
LBLUE='\033[01;34m'
LPURPLE='\033[01;35m'
LCYAN='\033[01;36m'
WHITE='\033[01;37m'


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
r_scope="(\([[:alnum:] \/-]+\))?"
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
