import json
import os
import logging
from typing import Dict, List, Any, Type, TypeVar, Generic, Optional
from pydantic import BaseModel
from datetime import datetime


T = TypeVar('T', bound=BaseModel)

class JsonDatabase(Generic[T]):
    """Simple JSON file-based database for storing model instances."""
    
    def __init__(self, file_path: str, model_class: Type[T]):
        self.file_path = file_path
        self.model_class = model_class
        self.data: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"db.{model_class.__name__.lower()}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Load data if file exists
        self._load_data()
    
    def _load_data(self) -> None:
        """Load data from JSON file if it exists."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self.logger.debug(f"Loaded {len(self.data)} records from {self.file_path}")
            else:
                self.data = {}
                self.logger.debug(f"No database file found at {self.file_path}, starting with empty database")
        except Exception as e:
            self.logger.error(f"Error loading data from {self.file_path}: {e}")
            self.data = {}
    
    def _save_data(self) -> None:
        """Save data to JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=self._json_serializer)
            self.logger.debug(f"Saved {len(self.data)} records to {self.file_path}")
        except Exception as e:
            self.logger.error(f"Error saving data to {self.file_path}: {e}")
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for handling datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def get(self, item_id: str) -> Optional[T]:
        """Get item by ID."""
        if item_id in self.data:
            try:
                return self.model_class.parse_obj(self.data[item_id])
            except Exception as e:
                self.logger.error(f"Error parsing item {item_id}: {e}")
                return None
        return None
    
    def get_all(self) -> List[T]:
        """Get all items."""
        result = []
        for item_id, item_data in self.data.items():
            try:
                result.append(self.model_class.parse_obj(item_data))
            except Exception as e:
                self.logger.error(f"Error parsing item {item_id}: {e}")
        return result
    
    def create(self, item: T) -> bool:
        """Create a new item."""
        try:
            # Extract ID field - assumes item has an attribute ending with '_id'
            id_field = next((f for f in item.__fields__ if f.endswith('_id')), None)
            if not id_field:
                self.logger.error(f"Cannot create item: no ID field found in {self.model_class.__name__}")
                return False
            
            item_id = getattr(item, id_field)
            
            if item_id in self.data:
                self.logger.warning(f"Item with ID {item_id} already exists, use update instead")
                return False
            
            self.data[item_id] = item.dict()
            self._save_data()
            return True
        except Exception as e:
            self.logger.error(f"Error creating item: {e}")
            return False
    
    def update(self, item: T) -> bool:
        """Update an existing item."""
        try:
            # Extract ID field
            id_field = next((f for f in item.__fields__ if f.endswith('_id')), None)
            if not id_field:
                self.logger.error(f"Cannot update item: no ID field found in {self.model_class.__name__}")
                return False
            
            item_id = getattr(item, id_field)
            
            if item_id not in self.data:
                self.logger.warning(f"Item with ID {item_id} does not exist, use create instead")
                return False
            
            self.data[item_id] = item.dict()
            self._save_data()
            return True
        except Exception as e:
            self.logger.error(f"Error updating item: {e}")
            return False
    
    def delete(self, item_id: str) -> bool:
        """Delete an item by ID."""
        if item_id in self.data:
            del self.data[item_id]
            self._save_data()
            return True
        return False
    
    def query(self, **kwargs) -> List[T]:
        """Query items by attribute values."""
        result = []
        for item_id, item_data in self.data.items():
            match = True
            for key, value in kwargs.items():
                # Handle nested attributes with dot notation
                if '.' in key:
                    parts = key.split('.')
                    current = item_data
                    for part in parts:
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            match = False
                            break
                    if match and current != value:
                        match = False
                # Handle simple attributes
                elif key not in item_data or item_data[key] != value:
                    match = False
            
            if match:
                try:
                    result.append(self.model_class.parse_obj(item_data))
                except Exception as e:
                    self.logger.error(f"Error parsing item {item_id}: {e}")
        
        return result


class DatabaseManager:
    """Manager for accessing different database collections."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.databases = {}
        self.logger = logging.getLogger("DatabaseManager")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def get_database(self, model_class: Type[T], name: str = None) -> JsonDatabase[T]:
        """Get or create a database for a model class."""
        db_name = name or model_class.__name__.lower() + "s"
        if db_name not in self.databases:
            file_path = os.path.join(self.data_dir, f"{db_name}.json")
            self.databases[db_name] = JsonDatabase(file_path, model_class)
            self.logger.info(f"Created database: {db_name}")
        return self.databases[db_name]