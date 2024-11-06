import json
import requests
import pandas as pd
from typing import List, Dict, Optional
from .base import BaseDataCollector

class QuickDrawCollector(BaseDataCollector):
    def __init__(self, output_dir: str = "datasets/quickdraw"):
        super().__init__(output_dir)
        self.base_url = "https://storage.googleapis.com/quickdraw_dataset/full/simplified"
        self.metadata_url = "https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt"
    
    def get_categories(self) -> List[str]:
        """Obtiene lista de categorías disponibles"""
        response = requests.get(self.metadata_url)
        return response.text.splitlines()
    
    def download_category(self, category: str) -> Optional[List[Dict]]:
        """Descarga datos de una categoría específica"""
        try:
            url = f"{self.base_url}/{category}.ndjson"
            self.logger.info(f"Descargando {category} desde {url}")
            
            df = pd.read_json(url, lines=True)
            output_file = self.output_dir / f"{category}.json"
            
            processed_data = []
            for _, row in df.iterrows():
                processed_data.append({
                    'source': 'quickdraw',
                    'category': category,
                    'drawing': row['drawing'],
                    'word': row['word'],
                    'timestamp': row['timestamp'],
                    'countrycode': row['countrycode'],
                    'recognized': row['recognized']
                })
            
            with open(output_file, 'w') as f:
                json.dump(processed_data, f)
            
            return processed_data
        
        except Exception as e:
            self.logger.error(f"Error descargando {category}: {str(e)}")
            return None