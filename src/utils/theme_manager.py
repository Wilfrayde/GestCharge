from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    def __init__(self):
        self.light_palette = QPalette()
        self.dark_palette = self._create_dark_palette()
        
    def _create_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        return palette

    def apply_theme(self, window, is_dark_mode):
        # Charger le fichier de style
        style_file = QFile("src/resources/styles.qss")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = QTextStream(style_file).readAll()
        
        if is_dark_mode:
            QApplication.setPalette(self.dark_palette)
            window.theme_action.setText("☼")
            window.setProperty("class", "dark")
        else:
            QApplication.setPalette(self.light_palette)
            window.theme_action.setText("☾")
            window.setProperty("class", "light")
        
        window.setStyleSheet(style_sheet)
        window.style().unpolish(window)
        window.style().polish(window) 