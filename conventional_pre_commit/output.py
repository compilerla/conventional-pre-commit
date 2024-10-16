import os
from typing import List, Optional

from conventional_pre_commit import format


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


def fail(commit_msg):
    lines = [
        f"{Colors.LRED}[Bad commit message] >>{Colors.RESTORE} {commit_msg}"
        f"{Colors.YELLOW}Your commit message does not follow Conventional Commits formatting{Colors.RESTORE}",
        f"{Colors.LBLUE}https://www.conventionalcommits.org/{Colors.RESTORE}",
    ]
    return os.linesep.join(lines)


def verbose_arg():
    lines = [
        "",
        f"{Colors.YELLOW}Use the {Colors.RESTORE}--verbose{Colors.YELLOW} arg for more information{Colors.RESTORE}",
    ]
    return os.linesep.join(lines)


def fail_verbose(commit_msg: str, types=format.DEFAULT_TYPES, optional_scope=True, scopes: Optional[List[str]] = None):
    match = format.conventional_match(commit_msg, types, optional_scope, scopes)
    lines = [
        "",
        f"{Colors.YELLOW}Conventional Commit messages follow a pattern like:",
        "",
        f"{Colors.RESTORE}    type(scope): subject",
        "",
        "    extended body",
        "",
    ]

    groups = match.groupdict() if match else {}

    if optional_scope:
        groups.pop("scope", None)

    if not groups.get("body"):
        groups.pop("body", None)
        groups.pop("multi", None)
        groups.pop("sep", None)

    if groups.keys():
        lines.append(f"{Colors.YELLOW}Please correct the following errors:{Colors.RESTORE}")
        lines.append("")
        for group in [g for g, v in groups.items() if not v]:
            if group == "scope":
                if scopes:
                    lines.append(f"  - Expected value for 'scope' from: {','.join(scopes)}")
                else:
                    lines.append("  - Expected value for 'scope' but found none.")
            else:
                lines.append(f"  - Expected value for '{group}' but found none.")

    lines.extend(
        [
            "",
            f"{Colors.YELLOW}Run:{Colors.RESTORE}",
            "",
            "    git commit --edit --file=.git/COMMIT_EDITMSG",
            "",
            f"{Colors.YELLOW}to edit the commit message and retry the commit.{Colors.RESTORE}",
        ]
    )
    return os.linesep.join(lines)


def unicode_decode_error():
    return f"""
{Colors.LRED}[Bad commit message encoding]{Colors.RESTORE}

{Colors.YELLOW}conventional-pre-commit couldn't decode your commit message.
UTF-8 encoding is assumed, please configure git to write commit messages in UTF-8.
See {Colors.LBLUE}https://git-scm.com/docs/git-commit/#_discussion{Colors.YELLOW} for more.{Colors.RESTORE}
"""
