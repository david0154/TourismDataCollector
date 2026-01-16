"""
Data export utilities
"""
import json
import csv
import pandas as pd
from typing import List, Dict, Any

class DataExporter:
    def export_to_json(self, data: List[Dict[str, Any]], file_path: str):
        """Export data to JSON format"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def export_to_csv(self, data: List[Dict[str, Any]], file_path: str):
        """Export data to CSV format"""
        if not data:
            return
        
        keys = data[0].keys()
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    
    def export_to_excel(self, data: List[Dict[str, Any]], file_path: str):
        """Export data to Excel format"""
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine='openpyxl')
    
    def export_to_xml(self, data: List[Dict[str, Any]], file_path: str):
        """Export data to XML format"""
        import xml.etree.ElementTree as ET
        
        root = ET.Element("tourism_data")
        
        for item in data:
            record = ET.SubElement(root, "record")
            for key, value in item.items():
                element = ET.SubElement(record, key)
                element.text = str(value)
        
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
