# File: gui/themes.py

# Định nghĩa các bảng màu THEMES
THEMES = {
    "rainy_days": {
        "NAME": "Ngày Mưa",
        "MAIN_BG": "#2c3e50",
        "CARD_BG": "rgba(62, 83, 104, 0.95)",
        "TEXT_COLOR": "#ecf0f1",
        "ACCENT_COLOR_BUTTON": "#5dade2",
        "SECONDARY_BUTTON_BG": "#4a6572",
        "SECONDARY_BUTTON_HOVER_BG": "#527888",
        "SECONDARY_BUTTON_PRESSED_BG": "#3e5e70",
        "KEYBIND_BUTTON_BG": "#34495e",
        "KEYBIND_BUTTON_TEXT": "#bdc3c7",
        "KEYBIND_BUTTON_HOVER_BG": "#4a6572",
        "KEYBIND_BUTTON_PRESSED_BG": "#2c3e50",
        "BORDER_COLOR": "#1c2833",
        "GROUPBOX_BORDER_WIDTH": "1.5px",
        "INPUT_BG": "#3e5062",
        "INPUT_TEXT": "#ecf0f1",
        "TAB_BG": "rgba(52, 73, 94, 0.7)",
        "TAB_SELECTED_BG": "rgba(62, 83, 104, 0.95)",
        "TAB_TEXT": "#bdc3c7",
        "TAB_SELECTED_TEXT": "#ffffff",
        "SPLITTER_HANDLE": "#7f8c8d",
        "START_BUTTON_BG": "#27ae60",
        "STOP_BUTTON_BG": "#c0392b",
        "DEBUG_BG": "rgba(35, 43, 54, 0.9)",
        "ACTIVE_TOOL_BG": "#5dade2",
        "ACTIVE_TOOL_TEXT": "#ffffff",
    },
    "warm_sunsets": {
        "NAME": "Hoàng Hôn Ấm Áp",
        "MAIN_BG": "#fff0e1",
        "CARD_BG": "rgba(255, 230, 205, 0.98)",
        "TEXT_COLOR": "#503015",
        "ACCENT_COLOR_BUTTON": "#e67e22",
        "SECONDARY_BUTTON_BG": "#f39c12",
        "SECONDARY_BUTTON_HOVER_BG": "#f1b040",
        "SECONDARY_BUTTON_PRESSED_BG": "#d0890f",
        "KEYBIND_BUTTON_BG": "#ffe8cc",
        "KEYBIND_BUTTON_TEXT": "#826a51",
        "KEYBIND_BUTTON_HOVER_BG": "#fff2e0",
        "KEYBIND_BUTTON_PRESSED_BG": "#f5d5b0",
        "BORDER_COLOR": "#d35400",
        "GROUPBOX_BORDER_WIDTH": "1.5px",
        "INPUT_BG": "#fffdf0",
        "INPUT_TEXT": "#5d4037",
        "TAB_BG": "#fae5d3",
        "TAB_SELECTED_BG": "#fff5e8",
        "TAB_TEXT": "#8c7853",
        "TAB_SELECTED_TEXT": "#c06014",
        "SPLITTER_HANDLE": "#e5b48a",
        "START_BUTTON_BG": "#2ecc71",
        "STOP_BUTTON_BG": "#e74c3c",
        "DEBUG_BG": "rgba(253, 246, 227, 0.95)",
        "ACTIVE_TOOL_BG": "#e67e22",
        "ACTIVE_TOOL_TEXT": "#ffffff",
    }
}

def adjust_color(hex_color, amount):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    if lv == 6:
        try:
            rgb = tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
            return "#%02x%02x%02x" % new_rgb
        except ValueError:
            return "#000000"
    return hex_color