from pathlib import Path
from typing import Dict, List, Union
import json

class DatasetValidator:
    def __init__(self):
        self.required_fields = ['id', 'source', 'keywords']
        
    def validate_sample(self, sample: Dict) -> bool:
        """Valida un único ejemplo del dataset"""
        return all(field in sample for field in self.required_fields)
        
    def validate_dataset(self, dataset_path: Union[str, Path]) -> Dict:
        """Valida un dataset completo"""
        dataset_path = Path(dataset_path)
        results = {
            'valid_samples': 0,
            'invalid_samples': 0,
            'errors': []
        }
        
        with open(dataset_path) as f:
            data = json.load(f)
            
        for idx, sample in enumerate(data):
            if not self.validate_sample(sample):
                results['invalid_samples'] += 1
                results['errors'].append(f"Muestra {idx} inválida")
            else:
                results['valid_samples'] += 1
                
        return results