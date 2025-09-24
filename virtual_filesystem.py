#!/usr/bin/env python3
"""
Virtual File System for Vibespan.ai
Handles context and memory offloading without file system dependencies.
"""

import json
import base64
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VirtualFileSystem:
    """Virtual file system for storing agent context and memory"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.files: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"vfs.{tenant_id}")
    
    def _generate_path(self, category: str, filename: str) -> str:
        """Generate a virtual path for a file"""
        return f"/{self.tenant_id}/{category}/{filename}"
    
    def _encode_content(self, content: Any) -> str:
        """Encode content for storage"""
        if isinstance(content, (dict, list)):
            return base64.b64encode(json.dumps(content).encode()).decode()
        return base64.b64encode(str(content).encode()).decode()
    
    def _decode_content(self, encoded_content: str) -> Any:
        """Decode content from storage"""
        try:
            decoded = base64.b64decode(encoded_content.encode()).decode()
            return json.loads(decoded)
        except:
            return base64.b64decode(encoded_content.encode()).decode()
    
    def write_file(self, category: str, filename: str, content: Any, metadata: Optional[Dict] = None) -> str:
        """Write a file to the virtual file system"""
        path = self._generate_path(category, filename)
        
        file_data = {
            "path": path,
            "content": self._encode_content(content),
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "size": len(str(content)),
            "checksum": hashlib.md5(str(content).encode()).hexdigest()
        }
        
        self.files[path] = file_data
        self.logger.info(f"Written file: {path} ({file_data['size']} bytes)")
        
        return path
    
    def read_file(self, category: str, filename: str) -> Optional[Any]:
        """Read a file from the virtual file system"""
        path = self._generate_path(category, filename)
        
        if path not in self.files:
            self.logger.warning(f"File not found: {path}")
            return None
        
        file_data = self.files[path]
        content = self._decode_content(file_data["content"])
        
        self.logger.info(f"Read file: {path}")
        return content
    
    def list_files(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List files in the virtual file system"""
        if category:
            prefix = f"/{self.tenant_id}/{category}/"
            files = {k: v for k, v in self.files.items() if k.startswith(prefix)}
        else:
            prefix = f"/{self.tenant_id}/"
            files = {k: v for k, v in self.files.items() if k.startswith(prefix)}
        
        return [
            {
                "path": path,
                "filename": path.split("/")[-1],
                "category": path.split("/")[-2] if len(path.split("/")) > 2 else "unknown",
                "size": file_data["size"],
                "created_at": file_data["created_at"],
                "updated_at": file_data["updated_at"],
                "checksum": file_data["checksum"]
            }
            for path, file_data in files.items()
        ]
    
    def delete_file(self, category: str, filename: str) -> bool:
        """Delete a file from the virtual file system"""
        path = self._generate_path(category, filename)
        
        if path in self.files:
            del self.files[path]
            self.logger.info(f"Deleted file: {path}")
            return True
        
        self.logger.warning(f"File not found for deletion: {path}")
        return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        total_files = len(self.files)
        total_size = sum(file_data["size"] for file_data in self.files.values())
        
        categories = {}
        for path, file_data in self.files.items():
            parts = path.split("/")
            if len(parts) > 2:
                category = parts[-2]
                if category not in categories:
                    categories[category] = {"count": 0, "size": 0}
                categories[category]["count"] += 1
                categories[category]["size"] += file_data["size"]
        
        return {
            "tenant_id": self.tenant_id,
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": categories
        }

class AgentContextManager:
    """Manages agent context and memory using virtual file system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.vfs = VirtualFileSystem(tenant_id)
        self.logger = logging.getLogger(f"context.{tenant_id}")
    
    def save_agent_result(self, agent_name: str, result: Dict[str, Any]) -> str:
        """Save agent processing result"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name}_{timestamp}.json"
        
        metadata = {
            "agent_name": agent_name,
            "result_type": "agent_processing",
            "timestamp": timestamp
        }
        
        return self.vfs.write_file("agent_results", filename, result, metadata)
    
    def save_health_data(self, data_type: str, data: Dict[str, Any]) -> str:
        """Save health data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_type}_{timestamp}.json"
        
        metadata = {
            "data_type": data_type,
            "source": "user_input",
            "timestamp": timestamp
        }
        
        return self.vfs.write_file("health_data", filename, data, metadata)
    
    def save_pattern_insight(self, pattern: Dict[str, Any]) -> str:
        """Save pattern detection insight"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pattern_{timestamp}.json"
        
        metadata = {
            "insight_type": "pattern_detection",
            "timestamp": timestamp
        }
        
        return self.vfs.write_file("insights", filename, pattern, metadata)
    
    def save_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """Save health recommendation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recommendation_{timestamp}.json"
        
        metadata = {
            "recommendation_type": "health_advice",
            "timestamp": timestamp
        }
        
        return self.vfs.write_file("recommendations", filename, recommendation, metadata)
    
    def get_recent_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent insights"""
        files = self.vfs.list_files("insights")
        files.sort(key=lambda x: x["created_at"], reverse=True)
        return files[:limit]
    
    def get_recent_recommendations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent recommendations"""
        files = self.vfs.list_files("recommendations")
        files.sort(key=lambda x: x["created_at"], reverse=True)
        return files[:limit]
    
    def get_agent_history(self, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get agent processing history"""
        files = self.vfs.list_files("agent_results")
        if agent_name:
            files = [f for f in files if agent_name in f["filename"]]
        files.sort(key=lambda x: x["created_at"], reverse=True)
        return files
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of all stored context"""
        stats = self.vfs.get_storage_stats()
        
        return {
            "tenant_id": self.tenant_id,
            "storage_stats": stats,
            "recent_insights": len(self.get_recent_insights(5)),
            "recent_recommendations": len(self.get_recent_recommendations(5)),
            "total_agent_runs": len(self.get_agent_history()),
            "last_updated": datetime.now().isoformat()
        }

# Global context managers for each tenant
_context_managers: Dict[str, AgentContextManager] = {}

def get_context_manager(tenant_id: str) -> AgentContextManager:
    """Get or create context manager for tenant"""
    if tenant_id not in _context_managers:
        _context_managers[tenant_id] = AgentContextManager(tenant_id)
    return _context_managers[tenant_id]
