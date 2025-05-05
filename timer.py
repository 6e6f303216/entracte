from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PyQt6.QtCore import QTimer, Qt, QRect, QPoint, QByteArray, QBuffer, QIODeviceBase
from PyQt6.QtGui import QPainter, QColor, QFontDatabase, QIcon, QFont
import subprocess
import sys
from threading import Thread
#from support import MiningManager #You weren't supposed to see this. Or were you?
from settings import SettingsDialog
from utils import load_styles, read_theme, resource_path
from config import read_timer_config
from fonts_data import JETBRAINS_MONO
import base64


class PomodoroTimer(QWidget):
    def __init__(self, work_time, break_time, long_break_duration):
        super().__init__()
        self.work_time = work_time
        self.break_time = break_time
        self.long_break_duration = long_break_duration
        self.is_running = False
        self.mood_energy = False
        self.cycle_count = 1
        self.score = 0
        
        #self.mining_manager = MiningManager() #Oh my gosh, someone actually reads the source code? O_o
        
        self.config = read_timer_config()
        self.support = self.config.get("support", False)

        self.setWindowTitle("Entracte")
        self.setWindowIcon(QIcon(resource_path("assets/app.png")))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.normal_height = 100
        self.min_height = 60
        self.setFixedSize(140, self.min_height)
        self._is_dragging = False
        self._drag_position = QPoint()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.work_duration = self.work_time * 60
        self.break_duration = self.break_time * 60
        self.long_break_duration = self.long_break_duration * 60
        self.current_time = self.work_duration
        self.duration = self.current_time

        self.timer_label = QPushButton(f"{self.work_time if self.work_time >= 10 else '0'+str(self.work_time)}:00", self)
        self.timer_label.clicked.connect(self.open_settings)
        self.timer_label.setObjectName("timer_label")
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("", self)
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start_timer)
        self.buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("", self)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop_timer)
        self.buttons_layout.addWidget(self.stop_button)

        self.skip_button = QPushButton("󱞸", self)
        self.skip_button.setObjectName("skip_button")
        self.skip_button.clicked.connect(self.skip_current)
        self.buttons_layout.addWidget(self.skip_button)

        self.reset_button = QPushButton("", self)
        self.reset_button.setObjectName("reset")
        self.reset_button.clicked.connect(self.reset_timer)
        self.buttons_layout.addWidget(self.reset_button)

        self.layout.addLayout(self.buttons_layout)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.start_button.hide()
        self.stop_button.hide()
        self.skip_button.hide()
        self.reset_button.hide()
        
        self.load_fonts()
        load_styles(self)

    def load_fonts(self):
        try:
            font_data = base64.b64decode(JETBRAINS_MONO)
            byte_array = QByteArray(font_data)
            buffer = QBuffer(byte_array)
            buffer.open(QIODeviceBase.OpenModeFlag.ReadOnly)

            font_id = QFontDatabase.addApplicationFontFromData(buffer.data())
            if font_id == -1:
                print("❌ Wow, fonts are missing! Run for your lives!")
            else:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    font = QFont(families[0])
                    self.setFont(font)
        except Exception as e:
            print(e)

    def open_settings(self):
        settings_dialog = SettingsDialog(self.work_duration // 60, self.break_duration // 60, self.long_break_duration // 60, self.support, self.cycle_count, self.score)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            config = read_timer_config()
            self.work_duration = int(settings_dialog.work_input.text()) * 60
            self.break_duration = int(settings_dialog.break_input.text()) * 60
            self.long_break_duration = int(settings_dialog.long_break_input.text()) * 60
            self.cycle_count = int(settings_dialog.cycle_count_input.text())
            self.score = int(settings_dialog.score_input.text())
            
            self.support = config.get("support", False)

            if self.cycle_count % 8 == 0:
                self.duration = self.long_break_duration
            elif self.cycle_count % 2 == 0:
                self.duration = self.break_duration
            else:
                self.duration = self.work_duration
            self.current_time = self.duration
            self.update_label()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            if self.height() != self.min_height:
                self.setFixedHeight(self.min_height)
            self.start_button.hide()
            self.stop_button.hide()
            self.skip_button.hide()
            self.reset_button.hide()
            if not self.timer.isActive():
                self.timer.start(1000)

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.update_buttons_visibility()
            self.start_button.hide()
            self.update()

    def skip_current(self):
        self.timer.stop()
        self.is_running = False
        self.cycle_count += 1
        self.end_cycle()

    def reset_timer(self):
        self.stop_timer()
        self.current_time = self.work_duration
        self.update_label()

    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
            self.update()
            self.update_label()
        else:
            self.cycle_count += 1
            self.end_cycle()

    def run_lockscreen_script(self, mode: str, duration: int):
        def target():
            if sys.platform == "win32":
                subprocess.run([
                    "powershell",
                    "-ExecutionPolicy", "Bypass",
                    "-File",
                    resource_path("lockscreen.ps1"),
                    mode,
                    str(duration)
                ])
            else:
                subprocess.run([
                    "sh",
                    resource_path("lockscreen.sh"),
                    mode,
                    str(duration)
                ])
        Thread(target=target, daemon=True).start()
                
    def end_cycle(self):
        if self.cycle_count % 8 == 0:
            self.score += (self.work_duration - self.current_time) // 60
            self.current_time = self.long_break_duration
            self.duration = self.current_time
            self.stop_timer()
            self.start_timer()
            self.run_lockscreen_script("break", self.long_break_duration)

        elif self.cycle_count % 2 == 0:
            self.score += (self.work_duration - self.current_time) // 60
            self.stop_timer()
            self.current_time = self.break_duration
            self.duration = self.current_time
            self.start_timer()
            self.run_lockscreen_script("break", self.break_duration)

        else:
            self.current_time = self.work_duration
            self.duration = self.current_time
            self.stop_timer()
            self.run_lockscreen_script("work", self.work_duration)
            self.reset_timer()
        
        self.update_label()

    def update_label(self):
        minutes, seconds = divmod(self.current_time, 60)
        time_format = f"{minutes:02}:{seconds:02}"
        if self.timer_label.text() != time_format:
            self.timer_label.setText(time_format)

    def enterEvent(self, event):
        if self.height() != self.normal_height:
            self.setFixedHeight(self.normal_height)
        self.update_buttons_visibility()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.height() != self.min_height:
            self.setFixedHeight(self.min_height)
        self.start_button.hide()
        self.stop_button.hide()
        self.skip_button.hide()
        self.reset_button.hide()
        super().leaveEvent(event)

    def update_buttons_visibility(self):
        self.start_button.setVisible(not self.is_running)
        self.stop_button.setVisible(self.is_running)
        self.reset_button.setVisible(self.is_running)
        self.skip_button.setVisible(self.is_running)

    def paintEvent(self, event):
        painter = QPainter(self)
        current_theme = read_theme()
        if current_theme == "light":
            progress_color = QColor.fromHsl(216, 25, 217)
            bg_color = QColor.fromHsl(216, 25, 204)
        else:
            progress_color = QColor.fromHsl(216, 25, 38)
            bg_color = QColor.fromHsl(216, 25, 51)
        
        painter.fillRect(self.rect(), bg_color)
        height = int((self.current_time / self.duration) * self.height())
        painter.fillRect(QRect(0, self.height() - height, self.width(), height), progress_color)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self._is_dragging:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            event.accept()
