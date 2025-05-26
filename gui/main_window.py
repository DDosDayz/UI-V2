# File: gui/main_window.py

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QPushButton, QGroupBox, QTextEdit,
    QSplitter # QLineEdit, QCheckBox, QRadioButton, QGridLayout, QComboBox, QSizePolicy đã được chuyển vào các tab
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt

# Import từ các file mới
from .themes import THEMES, adjust_color # <<< ĐẢM BẢO IMPORT adjust_color TỪ ĐÂY
from .tabs.auto_tab import AutoTabWidget
from .tabs.setting_tab import SettingTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Công cụ AI Maple")
        self.setFixedWidth(800)
        self.setMaximumHeight(1000)
        self.resize(800, 950)
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.is_bot_running = False
        self.current_theme = "rainy_days"

        # Nút Start/Stop được tạo ở đây để AutoTabWidget có thể tham chiếu đến nó
        self.start_stop_button = QPushButton()
        self.start_stop_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.start_stop_button.setFixedHeight(35)
        self.start_stop_button.clicked.connect(self._toggle_bot_state)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self._setup_header()
        self._setup_main_content_and_tabs()
        self._setup_debug_log()
        
        self._apply_theme()
        self._update_start_stop_button_style()


    def _get_current_palette(self):
        return THEMES[self.current_theme]

    def _apply_theme(self):
        palette = self._get_current_palette()
        main_stylesheet = f"""
            QMainWindow#MainWindow {{
                background-color: {palette["MAIN_BG"]};
                color: {palette["TEXT_COLOR"]};
                font-family: Segoe UI;
            }}
            QWidget {{
                background-color: transparent;
                color: {palette["TEXT_COLOR"]};
                font-family: Segoe UI;
            }}
            QGroupBox {{
                background-color: {palette["CARD_BG"]};
                border: {palette["GROUPBOX_BORDER_WIDTH"]} solid {palette["BORDER_COLOR"]};
                border-radius: 8px; margin-top: 10px; padding-top: 20px;
                font-size: 10pt; font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 5px 10px; background-color: {adjust_color(palette["CARD_BG"], 10 if self.current_theme == "rainy_days" else -10)};
                border: 1px solid {palette["BORDER_COLOR"]};
                border-bottom: 1px solid {palette["BORDER_COLOR"]};
                border-top-left-radius: 7px; border-top-right-radius: 7px;
                color: {palette["TEXT_COLOR"]};
            }}
            QLineEdit, QComboBox {{
                background-color: {palette["INPUT_BG"]}; color: {palette["INPUT_TEXT"]};
                border: 1px solid {palette["BORDER_COLOR"]}; border-radius: 4px;
                padding: 6px; min-height: 22px;
            }}
            QTextEdit#DebugLog {{
                 background-color: {palette["DEBUG_BG"]}; color: {palette["TEXT_COLOR"]};
                 border: 1px solid {palette["BORDER_COLOR"]}; border-radius: 4px; padding: 5px;
            }}
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
                border: 1.5px solid {palette["ACCENT_COLOR_BUTTON"]};
            }}
            QPushButton {{
                background-color: {palette["ACCENT_COLOR_BUTTON"]};
                color: {"#ffffff"};
                border: none; border-radius: 6px;
                padding: 7px 13px; font-weight: 500; min-height: 22px;
            }}
            QPushButton:hover {{
                background-color: {adjust_color(palette["ACCENT_COLOR_BUTTON"], -20)};
            }}
            QPushButton:pressed {{
                background-color: {adjust_color(palette["ACCENT_COLOR_BUTTON"], -40)};
                border: 1px solid {adjust_color(palette["ACCENT_COLOR_BUTTON"], -60)};
                padding-top: 8px; padding-bottom: 6px;
            }}
            QPushButton#SecondaryButton, QPushButton#MinimapToolButton, QPushButton#KeybindingButtonUnassigned {{
                background-color: {palette["SECONDARY_BUTTON_BG"]};
                color: {palette["TEXT_COLOR"]};
                border: 1px solid {adjust_color(palette["SECONDARY_BUTTON_BG"], -30)};
                font-style: {"italic" if "KeybindingButtonUnassigned" in "QPushButton#KeybindingButtonUnassigned" else "normal"};
            }}
            QPushButton#SecondaryButton:hover, QPushButton#KeybindingButtonUnassigned:hover, QPushButton#MinimapToolButton:hover {{
                background-color: {palette["SECONDARY_BUTTON_HOVER_BG"]};
                border: 1px solid {adjust_color(palette["SECONDARY_BUTTON_HOVER_BG"], -30)};
            }}
            QPushButton#SecondaryButton:pressed, QPushButton#KeybindingButtonUnassigned:pressed, QPushButton#MinimapToolButton:pressed {{
                background-color: {palette["SECONDARY_BUTTON_PRESSED_BG"]};
                border: 1px solid {adjust_color(palette["SECONDARY_BUTTON_PRESSED_BG"], -40)};
                padding-top: 8px; padding-bottom: 6px;
            }}
            QPushButton#MinimapToolButtonActive {{
                background-color: {palette["ACTIVE_TOOL_BG"]};
                color: {palette["ACTIVE_TOOL_TEXT"]};
                border: 1px solid {adjust_color(palette["ACTIVE_TOOL_BG"], -40)};
                font-weight: bold;
            }}
            QPushButton#MinimapToolButtonActive:hover {{
                background-color: {adjust_color(palette["ACTIVE_TOOL_BG"], -20)};
            }}
            QPushButton#MinimapToolButtonActive:pressed {{
                background-color: {adjust_color(palette["ACTIVE_TOOL_BG"], -40)};
                padding-top: 8px; padding-bottom: 6px;
            }}
            QTabWidget::pane {{ border-top: 1px solid {palette["BORDER_COLOR"]}; background-color: transparent; }}
            QTabBar::tab {{
                background-color: {palette["TAB_BG"]}; border: 1px solid {palette["BORDER_COLOR"]};
                border-bottom: none; padding: 8px 20px; margin-right: 2px;
                border-top-left-radius: 6px; border-top-right-radius: 6px;
                color: {palette["TAB_TEXT"]}; font-size: 9pt; font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {palette["TAB_SELECTED_BG"]}; color: {palette["TAB_SELECTED_TEXT"]};
                font-weight: bold; border-bottom: 1px solid {palette["TAB_SELECTED_BG"]};
            }}
            QSplitter::handle {{ background-color: {palette["SPLITTER_HANDLE"]}; }}
            QSplitter::handle:vertical {{ height: 5px; }}
            QLabel, QRadioButton, QCheckBox {{ color: {palette["TEXT_COLOR"]}; background-color: transparent; padding: 2px; }}
        """
        self.setStyleSheet(main_stylesheet)

        self.central_widget.setStyleSheet("background-color: transparent;")
        if hasattr(self, 'top_widget') and self.top_widget:
             self.top_widget.setStyleSheet("background-color: transparent;")

        if hasattr(self, 'tab_auto_widget') and self.tab_auto_widget:
            self.tab_auto_widget.setStyleSheet("background-color: transparent;")
            if hasattr(self.tab_auto_widget, '_update_minimap_toolbar_style_internal'):
                self.tab_auto_widget._update_minimap_toolbar_style_internal()
            if hasattr(self.tab_auto_widget, 'call_update_start_stop_button_style'):
                 self.tab_auto_widget.call_update_start_stop_button_style() # Gọi qua hàm mới

        if hasattr(self, 'tab_setting_widget') and self.tab_setting_widget:
            self.tab_setting_widget.setStyleSheet("background-color: transparent;")

        self._update_start_stop_button_style()


    def _toggle_theme(self):
        if self.current_theme == "rainy_days":
            self.current_theme = "warm_sunsets"
        else:
            self.current_theme = "rainy_days"
        self._apply_theme()
        self.add_log(f"Theme đã đổi thành: {THEMES[self.current_theme]['NAME']}")


    def _setup_header(self):
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 0, 0, 10)
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("🍁")
            logo_label.setFont(QFont("Segoe UI Emoji", 20))
        header_layout.addWidget(logo_label)
        title_label = QLabel("Công cụ AI Maple")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("margin-left: 5px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.theme_button = QPushButton("☀️/🌙")
        self.theme_button.setFixedWidth(60)
        self.theme_button.setObjectName("SecondaryButton") # Giữ lại nếu muốn style nút phụ
        self.theme_button.setToolTip("Đổi Theme Giao Diện")
        self.theme_button.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_button)
        self.main_layout.addLayout(header_layout)

    def _setup_main_content_and_tabs(self):
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_layout.addWidget(self.splitter, 1)

        self.top_widget = QWidget()
        top_layout = QVBoxLayout(self.top_widget)
        top_layout.setContentsMargins(0,0,0,0)
        self.tabs = QTabWidget()
        top_layout.addWidget(self.tabs)
        self.splitter.addWidget(self.top_widget)

        # Truyền start_stop_button đã tạo trong __init__ vào AutoTabWidget
        self.tab_auto_widget = AutoTabWidget(main_window=self, start_stop_button_ref=self.start_stop_button)
        self.tab_setting_widget = SettingTabWidget(main_window=self)
        
        self.tabs.addTab(self.tab_auto_widget, "🎮 Tự động")
        self.tabs.addTab(self.tab_setting_widget, "⚙️ Cài đặt")

    def _setup_debug_log(self):
        debug_group = self._create_styled_groupbox("Nhật ký Gỡ lỗi", "🐞")
        debug_layout = QVBoxLayout(debug_group)
        debug_layout.setContentsMargins(5,5,5,5)
        self.debug_log = QTextEdit()
        self.debug_log.setObjectName("DebugLog")
        self.debug_log.setReadOnly(True)
        self.debug_log.setPlaceholderText("Các thông báo hoạt động của bot sẽ hiện ở đây...")
        self.debug_log.setFont(QFont("Consolas", 9))
        debug_layout.addWidget(self.debug_log)
        self.splitter.addWidget(debug_group)
        self.splitter.setSizes([600, 280])

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.debug_log.append(f"[{timestamp}] {message}")
        self.debug_log.verticalScrollBar().setValue(self.debug_log.verticalScrollBar().maximum())

    def _create_styled_groupbox(self, title, icon_text=""):
        return QGroupBox(f"{icon_text} {title}")

    def _toggle_bot_state(self):
        self.is_bot_running = not self.is_bot_running
        self.add_log(f"Trạng thái bot đã đổi thành: {'ĐANG CHẠY' if self.is_bot_running else 'ĐÃ DỪNG'}")
        self._update_start_stop_button_style()

    def _update_start_stop_button_style(self):
        palette = self._get_current_palette()
        if self.is_bot_running:
            self.start_stop_button.setText("DỪNG LẠI")
            self.start_stop_button.setStyleSheet(f"background-color: {palette['STOP_BUTTON_BG']}; color: white; border: none; padding: 8px; font-weight: bold;")
        else:
            self.start_stop_button.setText("BẮT ĐẦU")
            self.start_stop_button.setStyleSheet(f"background-color: {palette['START_BUTTON_BG']}; color: white; border: none; padding: 8px; font-weight: bold;")

    def on_scan_button_clicked(self):
        self.add_log("Bắt đầu quét màn hình...")
        QApplication.processEvents()
        self.add_log("Quét màn hình hoàn tất.")

    def on_find_window_clicked(self):
        self.add_log("Đang tìm cửa sổ game...")
        QApplication.processEvents()
        self.add_log("Đã tìm thấy cửa sổ: MapleStory.exe (ví dụ)")