from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QSizePolicy, QCheckBox, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from config import write_timer_config, read_timer_config
from utils import load_styles, toggle_theme, resource_path

class SettingsDialog(QDialog):
    def __init__(self, work_duration, break_duration, long_break_duration, support, cycle_count, score):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowTitle("Entracte")
        self.setWindowIcon(QIcon(resource_path("assets/app.png")))
        self.setFixedSize(200, 330)
        self.layout = QFormLayout()

        self.work_input = QLineEdit(self)
        self.work_input.setText(str(work_duration))
        self.layout.addRow("Work:", self.work_input)

        self.break_input = QLineEdit(self)
        self.break_input.setText(str(break_duration))
        self.layout.addRow("Break:", self.break_input)

        self.long_break_input = QLineEdit(self)
        self.long_break_input.setText(str(long_break_duration))
        self.layout.addRow("Rest:", self.long_break_input)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addRow(separator)

        self.cycle_count_input = QLineEdit(self)
        self.cycle_count_input.setText(str(cycle_count))
        self.layout.addRow("Cycle:", self.cycle_count_input)

        self.score_input = QLineEdit(self)
        self.score_input.setText(str(score))
        self.layout.addRow("Score:", self.score_input)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addRow(separator2)

        self.support_checkbox = QCheckBox("Support future", self)
        self.support_checkbox.setChecked(support) 
        self.layout.addRow(self.support_checkbox)

        self.save_button = QPushButton("Save", self)
        self.save_button.setObjectName("save_button")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.layout.addRow(self.save_button)

        self.theme_button = QPushButton("Toggle Theme", self)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.layout.addRow(self.theme_button)

        self.setLayout(self.layout)
        load_styles(self)

    def save_settings(self):
        work_duration = int(self.work_input.text())
        break_duration = int(self.break_input.text())
        long_break_duration = int(self.long_break_input.text())

        support = self.support_checkbox.isChecked()

        config = read_timer_config()
        config.update({
            "work_duration": work_duration,
            "break_duration": break_duration,
            "long_break_duration": long_break_duration,
            "support": support
        })
        write_timer_config(config)

        load_styles(self)

        self.accept()

    def toggle_theme(self):
        theme = toggle_theme()
        self.update_styles()

    def update_styles(self):
        load_styles(self)
