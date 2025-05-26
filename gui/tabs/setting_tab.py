# File: gui/tabs/setting_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QGroupBox, QGridLayout, QComboBox,
    QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SettingTabWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Cấu hình Game ---
        game_config_group = self._create_styled_groupbox("Cấu hình Game", "🎮")
        game_config_layout = QHBoxLayout(game_config_group)
        game_config_layout.setSpacing(10)
        game_config_layout.addWidget(QLabel("Cửa sổ Game:"))
        game_window_input = QLineEdit("MapleStory.exe")
        game_window_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        game_config_layout.addWidget(game_window_input)
        find_window_button = QPushButton("Tìm Cửa sổ")
        find_window_button.setObjectName("SecondaryButton")
        if self.main_window:
            find_window_button.clicked.connect(self.main_window.on_find_window_clicked)
        game_config_layout.addWidget(find_window_button)
        layout.addWidget(game_config_group)

        # --- Gán Phím Tắt ---
        keybinding_group = self._create_styled_groupbox("Gán Phím Tắt", "🔑")
        keybinding_main_layout = QVBoxLayout(keybinding_group)
        keybinding_main_layout.setSpacing(8)
        keybinding_grid_layout = QGridLayout()
        keybinding_grid_layout.setSpacing(10)
        keybinding_items = ["Tấn công:", "Nhảy:", "Lướt:", "Biến / Nhảy kép:"]
        for i, item_text in enumerate(keybinding_items):
            row, col = divmod(i, 2)
            item_layout = QHBoxLayout()
            label = QLabel(item_text)
            label.setFixedWidth(120)
            label.setFont(QFont("Segoe UI", 9))
            item_layout.addWidget(label)
            key_button = QPushButton("[Chưa Gán]")
            key_button.setObjectName("KeybindingButtonUnassigned")
            key_button.setFixedWidth(150)
            key_button.setFont(QFont("Segoe UI", 9))
            item_layout.addWidget(key_button)
            item_layout.addStretch()
            keybinding_grid_layout.addLayout(item_layout, row, col)
        keybinding_main_layout.addLayout(keybinding_grid_layout)
        keybinding_main_layout.addSpacing(10)

        class_logic_label = QLabel("Logic cho Hệ Phái:")
        class_logic_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        keybinding_main_layout.addWidget(class_logic_label)
        class_options_layout = QHBoxLayout()
        class_options_layout.setSpacing(5)
        classes = ["Chiến Binh", "Cung Thủ", "Pháp Sư", "Hệ Phái 1", "Hệ Phái 2"]
        self.class_radio_buttons = [] # Nên quản lý trong MainWindow nếu cần truy cập từ ngoài
        class_options_layout.addStretch(1)
        for class_name in classes:
            radio_button = QRadioButton(class_name)
            radio_button.setFont(QFont("Segoe UI", 9))
            self.class_radio_buttons.append(radio_button)
            class_options_layout.addWidget(radio_button)
            class_options_layout.addStretch(1)
        if self.class_radio_buttons:
            self.class_radio_buttons[0].setChecked(True)
        keybinding_main_layout.addLayout(class_options_layout)
        layout.addWidget(keybinding_group)

        # --- Phân Tích & Mục Tiêu ---
        targeting_group = self._create_styled_groupbox("Phân Tích & Mục Tiêu", "🎯")
        targeting_layout = QVBoxLayout(targeting_group)
        scan_button = QPushButton("Quét Màn Hình")
        scan_button.setObjectName("SecondaryButton")
        if self.main_window:
            scan_button.clicked.connect(self.main_window.on_scan_button_clicked)
        targeting_layout.addWidget(scan_button)
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Ưu Tiên Mục Tiêu:"))
        priority_combo = QComboBox()
        priority_combo.addItems(["Gần Nhất", "HP Thấp Nhất", "Ưu Tiên Boss"])
        priority_layout.addWidget(priority_combo)
        targeting_layout.addLayout(priority_layout)
        manual_target_button = QPushButton("Chọn Mục Tiêu Thủ Công")
        manual_target_button.setObjectName("SecondaryButton")
        targeting_layout.addWidget(manual_target_button)
        layout.addWidget(targeting_group)

        # --- Quản Lý Cấu Hình ---
        profile_group = self._create_styled_groupbox("Quản Lý Cấu Hình", "⚙️")
        profile_layout = QVBoxLayout(profile_group)
        import_export_layout = QHBoxLayout()
        import_button = QPushButton("Nhập")
        import_button.setObjectName("SecondaryButton")
        export_button = QPushButton("Xuất")
        export_button.setObjectName("SecondaryButton")
        import_export_layout.addWidget(import_button)
        import_export_layout.addWidget(export_button)
        profile_layout.addLayout(import_export_layout)
        layout.addWidget(profile_group)

        layout.addStretch()

    def _create_styled_groupbox(self, title, icon_text=""):
        if self.main_window:
            return self.main_window._create_styled_groupbox(title, icon_text)
        return QGroupBox(f"{icon_text} {title}") # Fallback