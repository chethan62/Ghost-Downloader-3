"""Entry point for Ghost Downloader 3."""
import os
import sys
import traceback


def _ensure_desktop_shortcut() -> None:
    """Create .desktop launcher + icon if they don't exist."""
    import pkgutil

    desktop_dir = os.path.expanduser("~/.local/share/applications")
    icon_dir = os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps")
    desktop_file = os.path.join(desktop_dir, "ghost-downloader-3.desktop")
    icon_file = os.path.join(icon_dir, "ghost-downloader-3.png")

    if not os.path.exists(icon_file):
        os.makedirs(icon_dir, exist_ok=True)
        try:
            data = pkgutil.get_data("app.assets", "logo.png")
            if data:
                with open(icon_file, "wb") as f:
                    f.write(data)
        except Exception:
            pass

    if not os.path.exists(desktop_file):
        os.makedirs(desktop_dir, exist_ok=True)
        with open(desktop_file, "w") as f:
            f.write("""[Desktop Entry]
Type=Application
Name=Ghost Downloader 3
Comment=AI-powered cross-platform multi-protocol downloader
Exec=Ghost-Downloader-3
Icon=ghost-downloader-3
Terminal=false
Categories=Network;FileTransfer;
""")
        print("Created application shortcut: Ghost Downloader 3")


def main() -> int:
    """Launch Ghost Downloader 3."""
    _ensure_desktop_shortcut()

    from loguru import logger
    from app.config.paths import APP_DATA_DIR

    logger.add(f"{APP_DATA_DIR}/GhostDownloader.log", rotation="512 KB")

    def _exception_hook(etype, value, tb):
        info = (etype, value, tb)
        logger.opt(exception=info).error("Unhandled application exception")
        if "__compiled__" not in globals():
            sys.__excepthook__(*info)

    sys.excepthook = _exception_hook

    if sys.platform == "win32":
        from app.platform.hidden_subprocess import setupHiddenSubprocess
        setupHiddenSubprocess()

    import app.assets.resources  # noqa: F401
    from app.view.qfw_patch import patchFluentLabelThemeChanged
    from app.view.components.labels import IconBodyLabel
    from qfluentwidgets import qconfig
    from app.config.cfg import cfg
    from app.config.constants import VERSION

    patchFluentLabelThemeChanged()
    qconfig.themeChanged.connect(IconBodyLabel.clearCache)
    qconfig.load(f"{APP_DATA_DIR}/UserConfig.json", cfg)

    if sys.platform == "win32":
        from PySide6.QtGui import QFont
        from PySide6.QtWidgets import QApplication
        font = QFont()
        font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        QApplication.setFont(font)

    logger.info("Ghost Downloader v{} launched", VERSION)

    _start_app(is_silent="--silence" in sys.argv)
    return 0


def _start_app(is_silent=False):
    """Start the full Qt application. Originally from Ghost-Downloader-3.py."""
    from PySide6.QtGui import QIcon
    from app.config.cfg import cfg
    from app.config.constants import DESKTOP_ID
    from app.platform.application import SingletonApplication
    from app.services.browser_service import browserService
    from app.services.clipboard_listener import ClipboardListener
    from app.services.task_service import taskService
    from app.signal_bus import signalBus
    from app.startup import loadEngine, loadPacks, startEngine, bindNotifications, checkUpdateAtStartup, stopEngine
    from app.view.windows.main_window import MainWindow

    def exception_hook(etype, value, tb):
        from loguru import logger as log
        log.opt(exception=(etype, value, tb)).error("Unhandled application exception")
        message = "".join(traceback.format_exception(etype, value, tb)).rstrip()
        signalBus.exceptionCaught.emit(message)

    sys.excepthook = exception_hook
    app = SingletonApplication(sys.argv, DESKTOP_ID)
    app.setQuitOnLastWindowClosed(False)

    if sys.platform == "darwin":
        from app.view.shell.dock import setDockIconVisible
        setDockIconVisible(cfg.shouldShowDockIcon.value, activate=False)

    loadEngine(app)
    MainWindow.refreshThemeColor()
    window = MainWindow()

    if not is_silent:
        from qfluentwidgets import SplashScreen
        splash = SplashScreen(window.windowIcon(), window, enableShadow=False)
        splash.raise_()
        window.show()
        app.processEvents()

    loadPacks()
    window.setupPacks()
    startEngine()

    if not is_silent:
        splash.finish()

    from app.platform.windows import emptyWorkingSet

    def empty_working_set_if_idle():
        if window is None and taskService.runningCount() == 0:
            emptyWorkingSet()

    def on_window_destroyed():
        nonlocal window
        window = None
        empty_working_set_if_idle()

    window.destroyed.connect(on_window_destroyed)

    def show() -> MainWindow:
        nonlocal window
        if window is None:
            window = MainWindow()
            window.setupPacks()
            window.destroyed.connect(on_window_destroyed)
        window.show()
        from app.platform.desktop import raiseWindow
        raiseWindow(window)
        return window

    def on_browser_draft(tasks):
        nonlocal window
        if window is None:
            window = MainWindow()
            window.setupPacks()
            window.destroyed.connect(on_window_destroyed)
        window.addTasks(tasks)

    signalBus.activationRequested.connect(show)
    signalBus.openFileRequested.connect(lambda uris: show().addUrls(uris))
    signalBus.exceptionCaught.connect(lambda msg: show().alertException(msg))
    signalBus.updateAvailable.connect(lambda release: show()._onUpdateAvailable(release))
    browserService.taskDraftRequested.connect(on_browser_draft)
    browserService.pairRequested.connect(lambda req: show().confirmPair(req))

    def on_extension_updated(version):
        from qfluentwidgets import InfoBar, InfoBarPosition
        w = show()
        InfoBar.success(w.tr("Browser extension updated"), f"v{version}",
                        duration=3000, position=InfoBarPosition.BOTTOM_RIGHT, parent=w)

    browserService.extensionUpdated.connect(on_extension_updated)
    if cfg.isBrowserExtensionEnabled.value:
        browserService.start()
    cfg.isBrowserExtensionEnabled.valueChanged.connect(browserService.setEnabled)

    from app.services.aria2_rpc import aria2RpcServer
    aria2RpcServer.taskDraftRequested.connect(on_browser_draft)
    if cfg.isAria2RpcEnabled.value:
        aria2RpcServer.start()
    cfg.isAria2RpcEnabled.valueChanged.connect(aria2RpcServer.setEnabled)
    cfg.aria2RpcPort.valueChanged.connect(aria2RpcServer.setPort)

    clipboardListener = ClipboardListener(parent=app)
    cfg.isClipboardListenerEnabled.valueChanged.connect(clipboardListener.setEnabled)
    clipboardListener.setEnabled(cfg.isClipboardListenerEnabled.value)
    clipboardListener.urlsDetected.connect(lambda urls: show().addUrls(urls))

    if sys.platform == "darwin":
        from app.view.shell.mac_status_item import MacStatusItem
        from app.view.shell.dock import setupDock
        from app.services.speed_meter import speedMeter
        statusItem = MacStatusItem()
        statusItem.show()
        speedMeter.speedChanged.connect(statusItem.setSpeed)
        app.statusItem = statusItem
        setupDock()
    else:
        from app.view.shell.tray import SystemTrayIcon
        tray = SystemTrayIcon(QIcon(":/image/logo.png"), parent=app)
        tray.show()

    from app.platform.desktop_notification import init, notifyTaskCompleted, notifyDiskSpaceInsufficient
    from app.services.coroutine_runner import coroutineRunner
    coroutineRunner.submit(init())
    bindNotifications(notifyTaskCompleted, notifyDiskSpaceInsufficient)

    from app.services.plan import plan
    taskService.tasksAllCompleted.connect(plan.trigger)
    taskService.tasksAllCompleted.connect(empty_working_set_if_idle)

    if is_silent:
        empty_working_set_if_idle()

    checkUpdateAtStartup()
    app.aboutToQuit.connect(stopEngine)
    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())
