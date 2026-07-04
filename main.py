"""Entry point for Ghost Downloader 3."""
import os
import runpy
import sys


def _ensure_desktop_shortcut() -> None:
    """Create .desktop launcher + icon if they don't exist."""
    import shutil
    import pkgutil

    desktop_dir = os.path.expanduser("~/.local/share/applications")
    icon_dir = os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps")
    desktop_file = os.path.join(desktop_dir, "ghost-downloader-3.desktop")
    icon_file = os.path.join(icon_dir, "ghost-downloader-3.png")

    # Install icon
    if not os.path.exists(icon_file):
        os.makedirs(icon_dir, exist_ok=True)
        try:
            data = pkgutil.get_data("app.assets", "logo.png")
            if data:
                with open(icon_file, "wb") as f:
                    f.write(data)
        except Exception:
            pass

    if os.path.exists(desktop_file):
        return

    os.makedirs(desktop_dir, exist_ok=True)
    content = """[Desktop Entry]
Type=Application
Name=Ghost Downloader 3
Comment=AI-powered cross-platform multi-protocol downloader
Exec=Ghost-Downloader-3
Icon=ghost-downloader-3
Terminal=false
Categories=Network;FileTransfer;
"""
    with open(desktop_file, "w") as f:
        f.write(content)
    print("Created application shortcut: Ghost Downloader 3")


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
