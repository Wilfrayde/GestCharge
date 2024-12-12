import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.database.db_setup import setup_database

def main():
    setup_database()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
