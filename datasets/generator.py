from pathlib import Path
from typing import List, Dict, Union
import json
import shutil

class DatasetGenerator:
    def __init__(self, output_dir: Union[str, Path]):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_dataset(self, data: List[Dict], split_ratio: float = 0.8) -> Dict:
        """Genera datasets de entrenamiento y validación"""
        n_samples = len(data)
        n_train = int(n_samples * split_ratio)
        
        train_data = data[:n_train]
        val_data = data[n_train:]
        
        # Guardar splits
        splits = {
            'train': train_data,
            'val': val_data
        }
        
        for split_name, split_data in splits.items():
            split_dir = self.output_dir / split_name
            split_dir.mkdir(exist_ok=True)
            
            # Guardar metadata
            with open(split_dir / 'metadata.json', 'w') as f:
                json.dump(split_data, f)
                
        return splits


