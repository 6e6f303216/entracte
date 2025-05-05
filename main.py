import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from timer import PomodoroTimer
from config import read_timer_config, ensure_config_exists

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    ensure_config_exists()
    config = read_timer_config()
    work_time = config.get("work_duration", 25)
    break_time = config.get("break_duration", 5)
    long_break_duration = config.get("long_break_duration", 15)
    theme = config.get("theme", "light")

    app = QApplication(sys.argv)
    window = PomodoroTimer(work_time, break_time, long_break_duration)

    tray_icon = QSystemTrayIcon(QIcon(resource_path("assets/tray.png" if theme == "light" else "assets/tray_dark.png")), parent=app)

    menu = QMenu()

    restore_action = QAction("Restore")
    restore_action.triggered.connect(window.show)
    menu.addAction(restore_action)

    hide_action = QAction("Hide")
    hide_action.triggered.connect(window.hide)
    menu.addAction(hide_action)

    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)
    tray_icon.activated.connect(lambda reason: window.show() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)

    tray_icon.show()
    window.show()

    sys.exit(app.exec())
