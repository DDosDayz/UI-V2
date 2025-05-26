# File chính để khởi chạy ứng dụng
import sys
from PyQt6.QtWidgets import QApplication
# Đảm bảo import MainWindow từ đúng vị trí
from gui.main_window import MainWindow # Nếu main_window.py nằm trong gui/

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())