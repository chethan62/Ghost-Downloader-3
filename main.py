"""Entry point for Ghost Downloader 3."""
import os
import runpy
import sys


def _ensure_desktop_shortcut() -> None:
    """Create .desktop launcher if it doesn't exist."""
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    desktop_file = os.path.join(desktop_dir, "ghost-downloader-3.desktop")
    if os.path.exists(desktop_file):
        return

    repo_root = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(repo_root, "app", "assets", "logo.png")
    bin_path = os.environ.get("PIPX_BIN_DIR", os.path.join(os.path.expanduser("~/.local/bin"), "Ghost-Downloader-3"))

    os.makedirs(desktop_dir, exist_ok=True)
    content = f"""[Desktop Entry]
Type=Application
Name=Ghost Downloader 3
Comment=AI-boost cross-platform multi-protocol downloader
Icon={icon_path}
Exec=Ghost-Downloader-3
Terminal=false
Categories=Network;
StartupWMClass=Ghost-Downloader-3
"""
    with open(desktop_file, "w") as f:
        f.write(content)


def main() -> int:
    """Run Ghost-Downloader-3.py as a module."""
    _ensure_desktop_shortcut()
    repo_root = os.path.dirname(os.path.abspath(__file__))
    entry = os.path.join(repo_root, "Ghost-Downloader-3.py")
    sys.argv[0] = entry
    runpy.run_path(entry, run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
