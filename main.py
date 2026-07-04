"""Entry point for Ghost Downloader 3."""
import os
import runpy
import sys


def main() -> int:
    """Run Ghost-Downloader-3.py as a module."""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    entry = os.path.join(repo_root, "Ghost-Downloader-3.py")
    sys.argv[0] = entry
    runpy.run_path(entry, run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
