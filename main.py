"""
Tourism Data Collector
A comprehensive Windows application for collecting and validating tourism data across India
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Tourism Data Collector")
    app.setOrganizationName("Nexuzy Tech")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
