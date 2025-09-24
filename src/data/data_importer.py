#!/usr/bin/env python3
"""
Data Importer for Vibespan.ai
Imports existing health data into tenant-specific storage.
"""

import json
# import pandas as pd  # Will add later
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from ..auth.tenant_manager import tenant_manager

class DataImporter:
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.xlsx']
    
    def import_user_data(self, user_id: str, data_files: Dict[str, str]) -> Dict[str, Any]:
        """Import user's existing health data"""
        
        results = {
            "user_id": user_id,
            "imported_sources": [],
            "total_records": 0,
            "errors": []
        }
        
        # Get tenant data directory
        tenant_data_dir = tenant_manager.get_tenant_data_path(user_id, "raw")
        
        for source_name, file_path in data_files.items():
            try:
                # Import based on file type
                if file_path.endswith('.csv'):
                    records = self._import_csv(file_path, source_name)
                elif file_path.endswith('.json'):
                    records = self._import_json(file_path, source_name)
                elif file_path.endswith('.xlsx'):
                    records = self._import_excel(file_path, source_name)
                else:
                    results["errors"].append(f"Unsupported format: {file_path}")
                    continue
                
                # Save to tenant directory
                output_file = tenant_data_dir / f"{source_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
                with open(output_file, "w") as f:
                    json.dump(records, f, indent=2)
                
                # Add to tenant data sources
                tenant_manager.add_data_source(
                    user_id, 
                    source_name, 
                    {
                        "file_path": str(output_file),
                        "record_count": len(records),
                        "imported_at": datetime.utcnow().isoformat()
                    }
                )
                
                results["imported_sources"].append(source_name)
                results["total_records"] += len(records)
                
                # Log audit
                tenant_manager.log_audit(
                    user_id,
                    "data_imported",
                    {
                        "source": source_name,
                        "records": len(records),
                        "file_path": str(output_file)
                    }
                )
                
            except Exception as e:
                results["errors"].append(f"Error importing {source_name}: {str(e)}")
        
        return results
    
    def _import_csv(self, file_path: str, source_name: str) -> List[Dict[str, Any]]:
        """Import CSV file (simplified version)"""
        import csv
        
        records = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    "source": source_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": row
                }
                records.append(record)
        
        return records
    
    def _import_json(self, file_path: str, source_name: str) -> List[Dict[str, Any]]:
        """Import JSON file"""
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            records = []
            for item in data:
                record = {
                    "source": source_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": item
                }
                records.append(record)
        else:
            records = [{
                "source": source_name,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }]
        
        return records
    
    def _import_excel(self, file_path: str, source_name: str) -> List[Dict[str, Any]]:
        """Import Excel file (placeholder - will add pandas later)"""
        # For now, return empty list
        return []

# Global data importer instance
data_importer = DataImporter()
