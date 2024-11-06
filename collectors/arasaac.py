import requests
import json
from pathlib import Path
from typing import List, Dict
from .base import BaseDataCollector

class ArasaacCollector(BaseDataCollector):
    def __init__(self, output_dir: str = "datasets/arasaac"):
        super().__init__(output_dir)
        self.base_url = "https://api.arasaac.org/api"
    
    def search_pictograms(self, keyword: str, locale: str = 'en') -> List[Dict]:
        """Buscar pictogramas por palabra clave"""
        url = f"{self.base_url}/pictograms/{locale}/search/{keyword}"
        
        try:
            print(f"Buscando pictogramas para '{keyword}'...")
            response = requests.get(url)
            response.raise_for_status()
            results = response.json()
            print(f"Encontrados {len(results)} pictogramas")
            
            # Mostrar algunos detalles de los primeros resultados
            for i, result in enumerate(results[:3]):
                print(f"Pictograma {i+1}: ID={result['_id']}, Tags={result.get('tags', [])}")
            
            return results
            
        except Exception as e:
            print(f"Error en la búsqueda: {str(e)}")
            return []

    def download_pictogram(self, pictogram_id: int) -> Dict:
        """Descargar un pictograma específico"""
        try:
            # URL para imagen
            png_url = f"https://static.arasaac.org/pictograms/{pictogram_id}/{pictogram_id}_500.png"
            print(f"Descargando imagen desde: {png_url}")
            
            png_response = requests.get(png_url)
            
            if png_response.status_code == 200:
                # Crear directorio si no existe
                self.output_dir.mkdir(parents=True, exist_ok=True)
                
                # Guardar imagen
                image_path = self.output_dir / f"{pictogram_id}.png"
                image_path.write_bytes(png_response.content)
                print(f"Imagen guardada en: {image_path}")
                
                # Obtener y guardar metadata
                data = {
                    'id': pictogram_id,
                    'source': 'arasaac',
                    'image_path': str(image_path),
                    'url': png_url
                }
                
                metadata_path = self.output_dir / f"{pictogram_id}.json"
                with open(metadata_path, 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"Pictograma {pictogram_id} descargado exitosamente")
                return data
            else:
                print(f"Error {png_response.status_code} descargando imagen {pictogram_id}")
                return None
                
        except Exception as e:
            print(f"Error procesando pictograma {pictogram_id}: {str(e)}")
            return None