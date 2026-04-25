"""
Matrix Calculator — Entry Point
A premium desktop matrix calculator built with PyQt5 and NumPy.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ui_main_window import MainWindow
from ui_styles import MAIN_STYLESHEET


def main():
    # High DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Set global font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)

    # Apply stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
