import os

from conventional_pre_commit.format import ConventionalCommit


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"

    def __init__(self, enabled=True):
        self.enabled = enabled

    @property
    def blue(self):
        return self.LBLUE if self.enabled else ""

    @property
    def red(self):
        return self.LRED if self.enabled else ""

    @property
    def restore(self):
        return self.RESTORE if self.enabled else ""

    @property
    def yellow(self):
        return self.YELLOW if self.enabled else ""


def fail(commit: ConventionalCommit, use_color=True):
    c = Colors(use_color)
    lines = [
        f"{c.red}[Bad commit message] >>{c.restore} {commit.message}"
        f"{c.yellow}Your commit message does not follow Conventional Commits formatting{c.restore}",
        f"{c.blue}https://www.conventionalcommits.org/{c.restore}",
    ]
    return os.linesep.join(lines)


def verbose_arg(use_color=True):
    c = Colors(use_color)
    lines = [
        "",
        f"{c.yellow}Use the {c.restore}--verbose{c.yellow} arg for more information{c.restore}",
    ]
    return os.linesep.join(lines)


def fail_verbose(commit: ConventionalCommit, use_color=True):
    c = Colors(use_color)
    lines = [
        "",
        f"{c.yellow}Conventional Commit messages follow a pattern like:",
        "",
        f"{c.restore}    type(scope): subject",
        "",
        "    extended body",
        "",
    ]

    def _options(opts):
        formatted_opts = f"{c.yellow}, {c.blue}".join(opts)
        return f"{c.blue}{formatted_opts}"

    errors = commit.errors()
    if errors:
        lines.append(f"{c.yellow}Please correct the following errors:{c.restore}")
        lines.append("")
        for group in errors:
            if group == "type":
                type_opts = _options(commit.types)
                lines.append(f"{c.yellow}  - Expected value for {c.restore}type{c.yellow} from: {type_opts}")
            elif group == "scope":
                if commit.scopes:
                    scopt_opts = _options(commit.scopes)
                    lines.append(f"{c.yellow}  - Expected value for {c.restore}scope{c.yellow} from: {scopt_opts}")
                else:
                    lines.append(f"{c.yellow}  - Expected value for {c.restore}scope{c.yellow} but found none.{c.restore}")
            else:
                lines.append(f"{c.yellow}  - Expected value for {c.restore}{group}{c.yellow} but found none.{c.restore}")

    lines.extend(
        [
            "",
            f"{c.yellow}Run:{c.restore}",
            "",
            "    git commit --edit --file=.git/COMMIT_EDITMSG",
            "",
            f"{c.yellow}to edit the commit message and retry the commit.{c.restore}",
        ]
    )
    return os.linesep.join(lines)


def unicode_decode_error(use_color=True):
    c = Colors(use_color)
    return f"""
{c.red}[Bad commit message encoding]{c.restore}

{c.yellow}conventional-pre-commit couldn't decode your commit message.
UTF-8 encoding is assumed, please configure git to write commit messages in UTF-8.
See {c.blue}https://git-scm.com/docs/git-commit/#_discussion{c.yellow} for more.{c.restore}
"""
