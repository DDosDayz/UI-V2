# File: gui/tabs/auto_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QGroupBox, QGridLayout, QTextEdit,
    QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Import adjust_color từ themes.py cùng thư mục gui
from ..themes import adjust_color # <<< SỬA ĐỔI QUAN TRỌNG

# Dữ liệu mẫu cho skills
initial_skills = [
    {"id": 1, "key": "Q", "cooldown": "5", "enabled": True}, {"id": 2, "key": "W", "cooldown": "10", "enabled": True},
    {"id": 3, "key": "E", "cooldown": "3", "enabled": False},{"id": 4, "key": "R", "cooldown": "30", "enabled": True},
    {"id": 5, "key": "A", "cooldown": "0.5", "enabled": True},{"id": 6, "key": "S", "cooldown": "1", "enabled": False},
    {"id": 7, "key": "D", "cooldown": "15", "enabled": False},{"id": 8, "key": "F1", "cooldown": "60", "enabled": True},
    {"id": 9, "key": "Ctrl", "cooldown": "2", "enabled": True},
]

class AutoTabWidget(QWidget):
    def __init__(self, main_window=None, start_stop_button_ref=None):
        super().__init__()
        self.main_window = main_window
        self.start_stop_button_ref = start_stop_button_ref
        self.setStyleSheet("background-color: transparent;")

        self.active_minimap_tool = None
        self.minimap_tool_buttons = []

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        skills_group = self._create_styled_groupbox("Khu vực Kỹ năng", "⌨️")
        skills_layout = QGridLayout()
        skills_group.setLayout(skills_layout)

        for i, skill_data in enumerate(initial_skills):
            row, col = divmod(i, 3)
            skill_item_widget = QWidget()
            skill_item_layout = QHBoxLayout(skill_item_widget)
            skill_item_layout.setContentsMargins(0,0,0,0)
            skill_item_layout.setSpacing(8)

            key_input = QLineEdit(skill_data['key'])
            key_input.setFixedWidth(70)
            key_input.setMinimumHeight(28)
            key_input.setMaxLength(10)
            key_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            key_input.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            skill_item_layout.addWidget(key_input)

            cooldown_input = QLineEdit(skill_data['cooldown'])
            cooldown_input.setFixedWidth(55)
            cooldown_input.setMinimumHeight(28)
            cooldown_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cooldown_input.setFont(QFont("Segoe UI", 10))
            skill_item_layout.addWidget(cooldown_input)

            s_label = QLabel("giây")
            s_label.setFont(QFont("Segoe UI", 9))
            skill_item_layout.addWidget(s_label)

            enabled_checkbox = QCheckBox()
            enabled_checkbox.setChecked(skill_data['enabled'])
            enabled_checkbox.setStyleSheet("QCheckBox::indicator { width: 18px; height: 18px; }")
            skill_item_layout.addWidget(enabled_checkbox)
            skills_layout.addWidget(skill_item_widget, row, col)
        layout.addWidget(skills_group)

        map_editor_group = self._create_styled_groupbox("Logic với Minimap", "🗺️")
        editor_main_layout = QVBoxLayout(map_editor_group)
        editor_main_layout.setSpacing(10)

        canvas_placeholder = QLabel("Khu vực Bản đồ (Minimap)")
        canvas_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.main_window:
            palette = self.main_window._get_current_palette()
            canvas_placeholder.setStyleSheet(
                f"background-color: {adjust_color(palette['CARD_BG'], -10)}; " # <<< SỬA ĐỔI QUAN TRỌNG
                f"border: 2px dashed {palette['BORDER_COLOR']}; "
                f"border-radius: 6px; min-height: 200px;"
            )
        canvas_placeholder.setMinimumHeight(350)
        editor_main_layout.addWidget(canvas_placeholder, 1)

        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setSpacing(6)
        toolbar_layout.setContentsMargins(0,5,0,5)
        tools = [{"name": "Ngang", "icon": "↔"}, {"name": "Dọc", "icon": "↕"},
                 {"name": "Xuống", "icon": "↓"}, {"name": "Lên", "icon": "↑"},
                 {"name": "Quái", "icon": "M"}, {"name": "Đi", "icon": "G"},
                 {"name": "Cấm", "icon": "X"}]

        self.minimap_tool_buttons.clear()
        for tool_data in tools:
            tool_button = QPushButton(f"{tool_data['icon']} {tool_data['name']}")
            tool_button.setFont(QFont("Segoe UI", 8, QFont.Weight.Medium))
            tool_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tool_button.setObjectName("MinimapToolButton")
            tool_button.clicked.connect(
                lambda checked=False, name=tool_data['name']: self._on_minimap_tool_selected(name)
            )
            self.minimap_tool_buttons.append((tool_button, tool_data['name']))
            toolbar_layout.addWidget(tool_button)
        editor_main_layout.addWidget(toolbar_widget)

        if self.start_stop_button_ref: # Sử dụng tham chiếu đã truyền vào
            editor_main_layout.addWidget(self.start_stop_button_ref)
        else:
             # Fallback tạo nút tạm (không nên xảy ra)
             fallback_button = QPushButton("BẮT ĐẦU (Lỗi)")
             editor_main_layout.addWidget(fallback_button)


        layout.addWidget(map_editor_group)
        layout.addStretch()

    def _create_styled_groupbox(self, title, icon_text=""):
        if self.main_window:
            return self.main_window._create_styled_groupbox(title, icon_text)
        return QGroupBox(f"{icon_text} {title}")

    def _on_minimap_tool_selected(self, tool_name):
        self.active_minimap_tool = tool_name
        if self.main_window:
            self.main_window.add_log(f"Công cụ Minimap được chọn: {tool_name}")
        self._update_minimap_toolbar_style_internal()

    def _update_minimap_toolbar_style_internal(self):
        if not self.main_window:
            return

        palette = self.main_window._get_current_palette()
        for button, name in self.minimap_tool_buttons:
            is_active = (name == self.active_minimap_tool)
            button.setObjectName("MinimapToolButtonActive" if is_active else "MinimapToolButton")

            bg_color = palette["ACTIVE_TOOL_BG"] if is_active else palette["SECONDARY_BUTTON_BG"]
            text_color = palette["ACTIVE_TOOL_TEXT"] if is_active else palette["TEXT_COLOR"]
            # Gọi hàm adjust_color đã import trực tiếp
            border_color_val = adjust_color(bg_color, -40 if is_active else -30)
            font_weight = "bold" if is_active else "normal"
            hover_bg_color_val = adjust_color(bg_color, -20 if is_active else -15)
            pressed_bg_color_val = adjust_color(bg_color, -40 if is_active else -30)

            button.setStyleSheet(f"""
                QPushButton#{button.objectName()} {{
                    background-color: {bg_color}; color: {text_color};
                    border: 1px solid {border_color_val}; font-weight: {font_weight};
                    text-align: center; padding: 5px 6px; margin: 0px;
                }}
                QPushButton#{button.objectName()}:hover {{ background-color: {hover_bg_color_val}; }}
                QPushButton#{button.objectName()}:pressed {{ background-color: {pressed_bg_color_val}; padding-top: 6px; padding-bottom: 4px; }}
            """)

    def call_update_start_stop_button_style(self):
        if self.main_window and hasattr(self.main_window, '_update_start_stop_button_style'):
             self.main_window._update_start_stop_button_style()