import os


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
        "",
        f"{Colors.YELLOW}Use the {Colors.RESTORE}--verbose{Colors.YELLOW} arg for more information{Colors.RESTORE}",
    ]
    return os.linesep.join(lines)


def fail_verbose(commit_msg):
    lines = [
        "",
        f"{Colors.YELLOW}Run{Colors.RESTORE}",
        "",
        "    git commit --edit --file=.git/COMMIT_EDITMSG",
        "",
        f"{Colors.YELLOW}to edit the commit message and retry the commit.{Colors.RESTORE}",
    ]
    return os.linesep.join(lines)


def unicode_decode_error():
    return f"""
{Colors.LRED}[Bad commit message encoding]{Colors.RESTORE}

{Colors.YELLOW}conventional-pre-commit couldn't decode your commit message.
UTF-8 encoding is assumed, please configure git to write commit messages in UTF-8.
See {Colors.LBLUE}https://git-scm.com/docs/git-commit/#_discussion{Colors.YELLOW} for more.{Colors.RESTORE}
"""
