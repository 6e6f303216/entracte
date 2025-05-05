import os
import json
import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette

def is_dark_theme():
    palette = QApplication.palette()
    bg_color = palette.color(QPalette.ColorRole.Window)
    return bg_color.value() < 128

def get_config_path():
    system = platform.system().lower()
    if system == 'windows':
        config_dir = os.path.join(os.getenv('APPDATA'), 'entracte')
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "entracte")
    
    return os.path.join(config_dir, "entracte.json")

CONFIG_PATH = get_config_path()

def ensure_config_exists():
    theme = "dark" if is_dark_theme() else "light"
    default_config = {
        "work_duration": 25,
        "break_duration": 5,
        "long_break_duration": 15,
        "theme": theme,
        "support": False
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        write_timer_config(default_config)

def read_timer_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        ensure_config_exists()
        return read_timer_config()

def write_timer_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)

def read_theme():
    config = read_timer_config()
    return config.get("theme", "dark")

def write_theme(theme):
    config = read_timer_config()
    config["theme"] = theme
    write_timer_config(config)