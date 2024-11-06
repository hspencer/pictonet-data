from pathlib import Path
from typing import Union, Dict
import json

class DataNormalizer:
    def __init__(self):
        self.supported_formats = ['svg', 'json']
        
    def normalize_metadata(self, metadata: Dict) -> Dict:
        """Normaliza metadata a formato estándar"""
        return {
            'id': metadata.get('id') or metadata.get('hexcode'),
            'source': metadata.get('source'),
            'keywords': metadata.get('tags', []),
            'category': metadata.get('group') or metadata.get('category'),
            'description': metadata.get('annotation') or metadata.get('meaning')
        }
        
    def process_file(self, file_path: Union[str, Path]) -> Dict:
        """Procesa un archivo y retorna datos normalizados"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() not in [f'.{fmt}' for fmt in self.supported_formats]:
            raise ValueError(f"Formato no soportado: {file_path.suffix}")
            
        if file_path.suffix.lower() == '.json':
            with open(file_path) as f:
                data = json.load(f)
                return self.normalize_metadata(data)
                
        return {}