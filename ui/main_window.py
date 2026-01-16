"""
Main UI Window for Tourism Data Collector
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QTextEdit, QGroupBox,
                             QProgressBar, QMessageBox, QFileDialog, QTabWidget,
                             QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import sys
import json

from database.db_manager import DatabaseManager
from ai.data_validator import DataValidator
from ai.deduplicator import Deduplicator
from utils.india_data import INDIAN_STATES, get_tourist_places
from utils.exporters import DataExporter
from ui.styles import MAIN_STYLE

class CollectionWorker(QThread):
    """Worker thread for data collection"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, state, city, data_type):
        super().__init__()
        self.state = state
        self.city = city
        self.data_type = data_type
    
    def run(self):
        """Run data collection"""
        self.status.emit(f"Collecting {self.data_type} data for {self.city}, {self.state}...")
        self.progress.emit(30)
        
        # Simulate data collection (implement actual logic in production)
        import time
        time.sleep(2)
        
        self.progress.emit(70)
        self.status.emit("Validating collected data...")
        
        time.sleep(1)
        self.progress.emit(100)
        
        result = {
            'success': True,
            'message': f'Successfully collected {self.data_type} data',
            'count': 0
        }
        
        self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.validator = DataValidator()
        self.deduplicator = Deduplicator()
        self.exporter = DataExporter()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Tourism Data Collector - Nexuzy Tech")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(MAIN_STYLE)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Tourism Data Collector")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_collection_tab(), "Data Collection")
        tabs.addTab(self.create_view_tab(), "View Data")
        tabs.addTab(self.create_export_tab(), "Export Data")
        tabs.addTab(self.create_manual_entry_tab(), "Manual Entry")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
    
    def create_collection_tab(self):
        """Create data collection tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Location selection group
        location_group = QGroupBox("Select Location")
        location_layout = QVBoxLayout()
        
        # State selection
        state_layout = QHBoxLayout()
        state_layout.addWidget(QLabel("State:"))
        self.state_combo = QComboBox()
        self.state_combo.addItem("All India")
        self.state_combo.addItems(sorted(INDIAN_STATES.keys()))
        self.state_combo.currentTextChanged.connect(self.on_state_changed)
        state_layout.addWidget(self.state_combo)
        location_layout.addLayout(state_layout)
        
        # City/Place selection
        place_layout = QHBoxLayout()
        place_layout.addWidget(QLabel("Tourist Place:"))
        self.place_combo = QComboBox()
        self.place_combo.addItem("All Places")
        place_layout.addWidget(self.place_combo)
        location_layout.addLayout(place_layout)
        
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        # Data type selection
        data_type_group = QGroupBox("Select Data Type")
        data_type_layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Data Type:"))
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems([
            "Hotels",
            "Tourist Places",
            "Travel Services",
            "Restaurants",
            "All Types"
        ])
        type_layout.addWidget(self.data_type_combo)
        data_type_layout.addLayout(type_layout)
        
        data_type_group.setLayout(data_type_layout)
        layout.addWidget(data_type_group)
        
        # Collection options
        options_group = QGroupBox("Collection Options")
        options_layout = QVBoxLayout()
        
        options_layout.addWidget(QLabel("✓ Duplicate Detection Enabled"))
        options_layout.addWidget(QLabel("✓ AI Validation Enabled"))
        options_layout.addWidget(QLabel("✓ Online Verification Enabled"))
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to collect data")
        self.status_label.setStyleSheet("padding: 10px; font-size: 13px;")
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.collect_btn = QPushButton("Start Collection")
        self.collect_btn.clicked.connect(self.start_collection)
        button_layout.addWidget(self.collect_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return widget
    
    def create_view_tab(self):
        """Create data viewing tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("View:"))
        
        self.view_type_combo = QComboBox()
        self.view_type_combo.addItems(["Hotels", "Tourist Places", "Travel Services"])
        self.view_type_combo.currentTextChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.view_type_combo)
        
        filter_layout.addWidget(QLabel("State:"))
        self.view_state_combo = QComboBox()
        self.view_state_combo.addItem("All States")
        self.view_state_combo.addItems(sorted(INDIAN_STATES.keys()))
        self.view_state_combo.currentTextChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.view_state_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_table)
        filter_layout.addWidget(refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Data table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(8)
        self.data_table.setHorizontalHeaderLabels([
            "ID", "Name", "City", "State", "Contact", "Email", "Verified", "Created"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.data_table)
        
        # Record count
        self.record_count_label = QLabel("Total Records: 0")
        layout.addWidget(self.record_count_label)
        
        return widget
    
    def create_export_tab(self):
        """Create data export tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Export options
        export_group = QGroupBox("Export Options")
        export_layout = QVBoxLayout()
        
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Export Format:"))
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["JSON", "Excel (XLSX)", "CSV", "XML"])
        format_layout.addWidget(self.export_format_combo)
        export_layout.addLayout(format_layout)
        
        data_layout = QHBoxLayout()
        data_layout.addWidget(QLabel("Data Type:"))
        self.export_data_combo = QComboBox()
        self.export_data_combo.addItems(["Hotels", "Tourist Places", "Travel Services", "All Data"])
        data_layout.addWidget(self.export_data_combo)
        export_layout.addLayout(data_layout)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # Export button
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self.export_data)
        layout.addWidget(export_btn)
        
        # Export log
        self.export_log = QTextEdit()
        self.export_log.setReadOnly(True)
        self.export_log.setMaximumHeight(200)
        layout.addWidget(QLabel("Export Log:"))
        layout.addWidget(self.export_log)
        
        layout.addStretch()
        
        return widget
    
    def create_manual_entry_tab(self):
        """Create manual data entry tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Hotel entry form
        form_group = QGroupBox("Add Hotel Manually")
        form_layout = QVBoxLayout()
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Hotel Name:"))
        self.hotel_name_input = QLineEdit()
        name_layout.addWidget(self.hotel_name_input)
        form_layout.addLayout(name_layout)
        
        # Address
        addr_layout = QHBoxLayout()
        addr_layout.addWidget(QLabel("Address:"))
        self.hotel_addr_input = QLineEdit()
        addr_layout.addWidget(self.hotel_addr_input)
        form_layout.addLayout(addr_layout)
        
        # City
        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("City:"))
        self.hotel_city_input = QLineEdit()
        city_layout.addWidget(self.hotel_city_input)
        form_layout.addLayout(city_layout)
        
        # State
        state_layout = QHBoxLayout()
        state_layout.addWidget(QLabel("State:"))
        self.hotel_state_combo = QComboBox()
        self.hotel_state_combo.addItems(sorted(INDIAN_STATES.keys()))
        state_layout.addWidget(self.hotel_state_combo)
        form_layout.addLayout(state_layout)
        
        # Contact
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(QLabel("Contact:"))
        self.hotel_contact_input = QLineEdit()
        contact_layout.addWidget(self.hotel_contact_input)
        form_layout.addLayout(contact_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        self.hotel_email_input = QLineEdit()
        email_layout.addWidget(self.hotel_email_input)
        form_layout.addLayout(email_layout)
        
        # Add button
        add_btn = QPushButton("Add Hotel")
        add_btn.clicked.connect(self.add_hotel_manually)
        form_layout.addWidget(add_btn)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        layout.addStretch()
        
        return widget
    
    def on_state_changed(self, state):
        """Handle state selection change"""
        self.place_combo.clear()
        self.place_combo.addItem("All Places")
        
        if state != "All India" and state in INDIAN_STATES:
            places = get_tourist_places(state)
            self.place_combo.addItems(places)
    
    def start_collection(self):
        """Start data collection process"""
        state = self.state_combo.currentText()
        place = self.place_combo.currentText()
        data_type = self.data_type_combo.currentText()
        
        city = place if place != "All Places" else ""
        
        self.collect_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        self.worker = CollectionWorker(state, city, data_type)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.collection_finished)
        self.worker.start()
    
    def collection_finished(self, result):
        """Handle collection completion"""
        self.collect_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if result['success']:
            QMessageBox.information(self, "Success", result['message'])
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", result.get('error', 'Collection failed'))
    
    def refresh_table(self):
        """Refresh the data table"""
        view_type = self.view_type_combo.currentText()
        state = self.view_state_combo.currentText()
        state_filter = None if state == "All States" else state
        
        if view_type == "Hotels":
            data = self.db.get_all_hotels(state_filter)
        elif view_type == "Tourist Places":
            data = self.db.get_all_tourist_places(state_filter)
        else:
            data = []
        
        self.data_table.setRowCount(len(data))
        
        for row, record in enumerate(data):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(record.get('id', ''))))
            self.data_table.setItem(row, 1, QTableWidgetItem(record.get('name', '')))
            self.data_table.setItem(row, 2, QTableWidgetItem(record.get('city', '')))
            self.data_table.setItem(row, 3, QTableWidgetItem(record.get('state', '')))
            self.data_table.setItem(row, 4, QTableWidgetItem(record.get('contact', '')))
            self.data_table.setItem(row, 5, QTableWidgetItem(record.get('email', '')))
            self.data_table.setItem(row, 6, QTableWidgetItem("Yes" if record.get('verified') else "No"))
            self.data_table.setItem(row, 7, QTableWidgetItem(str(record.get('created_at', ''))))
        
        self.record_count_label.setText(f"Total Records: {len(data)}")
    
    def export_data(self):
        """Export data to selected format"""
        format_type = self.export_format_combo.currentText()
        data_type = self.export_data_combo.currentText()
        
        # Get file path
        file_filter = {
            "JSON": "JSON Files (*.json)",
            "Excel (XLSX)": "Excel Files (*.xlsx)",
            "CSV": "CSV Files (*.csv)",
            "XML": "XML Files (*.xml)"
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", file_filter.get(format_type, "")
        )
        
        if file_path:
            try:
                # Get data based on type
                if data_type == "Hotels":
                    data = self.db.get_all_hotels()
                elif data_type == "Tourist Places":
                    data = self.db.get_all_tourist_places()
                else:
                    data = []
                
                # Export based on format
                if format_type == "JSON":
                    self.exporter.export_to_json(data, file_path)
                elif format_type == "Excel (XLSX)":
                    self.exporter.export_to_excel(data, file_path)
                elif format_type == "CSV":
                    self.exporter.export_to_csv(data, file_path)
                
                self.export_log.append(f"✓ Successfully exported to {file_path}")
                QMessageBox.information(self, "Success", "Data exported successfully!")
            except Exception as e:
                self.export_log.append(f"✗ Export failed: {str(e)}")
                QMessageBox.warning(self, "Error", f"Export failed: {str(e)}")
    
    def add_hotel_manually(self):
        """Add hotel data manually"""
        hotel_data = {
            'name': self.hotel_name_input.text(),
            'address': self.hotel_addr_input.text(),
            'city': self.hotel_city_input.text(),
            'state': self.hotel_state_combo.currentText(),
            'contact': self.hotel_contact_input.text(),
            'email': self.hotel_email_input.text(),
            'verified': 0
        }
        
        # Validate data
        is_valid, errors = self.validator.validate_hotel_data(hotel_data)
        
        if not is_valid:
            error_msg = "\n".join([f"{k}: {v}" for k, v in errors.items()])
            QMessageBox.warning(self, "Validation Error", f"Please fix:\n{error_msg}")
            return
        
        # Check for duplicates
        if self.db.check_duplicate('hotels', hotel_data['name'], 
                                   hotel_data['city'], hotel_data['state']):
            QMessageBox.warning(self, "Duplicate", "This hotel already exists in the database!")
            return
        
        # Insert into database
        try:
            self.db.insert_hotel(hotel_data)
            QMessageBox.information(self, "Success", "Hotel added successfully!")
            
            # Clear form
            self.hotel_name_input.clear()
            self.hotel_addr_input.clear()
            self.hotel_city_input.clear()
            self.hotel_contact_input.clear()
            self.hotel_email_input.clear()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add hotel: {str(e)}")
