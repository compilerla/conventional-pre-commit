from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("conventional-pre-commit")
except PackageNotFoundError:
    # package is not installed
    pass
