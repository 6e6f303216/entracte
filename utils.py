import sys
import os
from PyQt6.QtWidgets import QApplication
from config import read_theme, write_theme

COMMON_STYLE = """
* {
    font-weight: bold;
}

#timer_label {
    font-size: 32px;
    font-family: "Noto Sans";
}

#counter {
    font-size: 17px;
}

QPushButton, #counter {
    font-size: 18px;
    padding: 5px;
    background: transparent;
    border: none;
}

#reset, #skip_button {
    font-size: 18px;
}

#start_button,
#stop_button,
#skip_button,
#reset, 
#save_button {
    font-family: "JetBrainsMono NF Medium";
}

QLabel {
    font-size: 16px;
}

QLineEdit {
    border-radius: 13px;
    padding: 5px;
    font-size: 16px;
}

#save_button {
    border-radius: 14px;
}

QCheckBox {
    font-size: 16px;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
}

"""

DARK_STYLE = COMMON_STYLE + """
* {
    color: hsl(216, 25%, 95%);
}

#start_button:hover,
#stop_button:hover,
#skip_button:hover,
#counter:hover, 
#reset:hover, 
#save_button:hover {
    color: hsl(240, 60%, 80%);
}

QDialog {
    background-color: hsl(216, 10%, 15%);
    color: hsl(216, 25%, 95%);
}

QLineEdit {
    background-color: hsl(216, 10%, 20%);
    color: hsl(216, 25%, 95%);
}

#save_button {
    background-color: hsl(216, 10%, 20%);
    color: hsl(216, 25%, 95%);
}

QCheckBox {
    color: hsl(216, 25%, 95%);
}

QCheckBox::indicator {
    border: 2px solid hsl(216, 10%, 20%);
    background: hsl(216, 10%, 15%);
}

QCheckBox::indicator:hover {
    border-color: hsl(240, 60%, 80%);
}

QCheckBox::indicator:checked {
    background: hsl(240, 60%, 80%);
    border-color: hsl(240, 60%, 80%);
}

QPushButton#save_button:hover {
    background-color: hsl(240, 60%, 80%);
    color: hsl(216, 10%, 15%);
}
"""

LIGHT_STYLE = COMMON_STYLE + """
* {
    color: hsl(216, 25%, 5%);
}

#start_button:hover,
#stop_button:hover,
#skip_button:hover,
#counter:hover, 
#reset:hover, 
#save_button:hover {
    color: hsl(240, 40%, 60%);
}

QDialog {
    background-color: hsl(216, 10%, 85%);
    color: hsl(216, 25%, 5%);
}

QLineEdit {
    background-color: hsl(216, 10%, 80%);
    color: hsl(216, 25%, 5%);
}

#save_button {
    background-color: hsl(216, 10%, 80%);
    color: hsl(216, 25%, 5%);
}

QCheckBox {
    color: hsl(216, 25%, 5%);
}

QCheckBox::indicator {
    border: 2px solid hsl(216, 10%, 80%);
    background: hsl(216, 10%, 85%);
}

QCheckBox::indicator:hover {
    border-color: hsl(240, 40%, 60%);
}

QCheckBox::indicator:checked {
    background: hsl(240, 40%, 60%);
    border-color: hsl(240, 40%, 60%);
}

QPushButton#save_button:hover {
    background-color: hsl(240, 40%, 60%);
    color: hsl(216, 10%, 85%);
}
"""


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

STYLE_MAP = {
    "light": LIGHT_STYLE,
    "dark": DARK_STYLE
}

def load_styles(widget):
    theme = read_theme()
    style = STYLE_MAP.get(theme, DARK_STYLE)
    widget.setStyleSheet(style)


def toggle_theme():
    new_theme = "dark" if read_theme() == "light" else "light"
    write_theme(new_theme)

    app = QApplication.instance()
    if app:
        for widget in app.allWidgets():
            load_styles(widget)

    return new_theme
