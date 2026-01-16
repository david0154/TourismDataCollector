"""
UI Styling for the application
"""

MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
}

QLabel {
    font-size: 13px;
    color: #333;
}

QLineEdit, QTextEdit, QComboBox {
    padding: 8px;
    border: 2px solid #E0E0E0;
    border-radius: 5px;
    background-color: white;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}

QTableWidget {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 5px;
    gridline-color: #E0E0E0;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #BBDEFB;
    color: #000;
}

QHeaderView::section {
    background-color: #2196F3;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QGroupBox {
    border: 2px solid #E0E0E0;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QProgressBar {
    border: 2px solid #E0E0E0;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4CAF50;
}

QTabWidget::pane {
    border: 1px solid #E0E0E0;
    border-radius: 5px;
    background-color: white;
}

QTabBar::tab {
    background-color: #E0E0E0;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: #2196F3;
    color: white;
}

QStatusBar {
    background-color: #2196F3;
    color: white;
}
"""
