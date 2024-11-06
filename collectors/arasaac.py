# src/pictonet_data/collectors/arasaac.py
import json
import requests
from typing import List, Dict, Optional
from .base import BaseDataCollector

class ArasaacCollector(BaseDataCollector):
    def __init__(self, output_dir: str = "datasets/arasaac"):
        super().__init__(output_dir)
        self.base_url = "https://api.arasaac.org/api/v1"
        self.locales = ['es', 'en', 'fr']
    
    def get_keywords(self, locale: str = 'en') -> List[str]:
        """Obtiene lista de keywords disponibles"""
        url = f"{self.base_url}/pictograms/{locale}/all"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [item['keyword'] for item in response.json()]
        except Exception as e:
            self.logger.error(f"Error obteniendo keywords: {str(e)}")
            return []
    
    def download_pictogram(self, pictogram_id: int, locales: Optional[List[str]] = None) -> Dict:
        """Descarga un pictograma específico y su metadata en varios idiomas"""
        locales = locales or self.locales
        pictogram_data = {'id': pictogram_id, 'translations': {}}
        
        try:
            # Descargar SVG
            svg_url = f"{self.base_url}/pictograms/{pictogram_id}"
            svg_response = requests.get(svg_url)
            
            if svg_response.status_code == 200:
                # Guardar SVG
                svg_file = self.output_dir / f"{pictogram_id}.svg"
                svg_file.write_bytes(svg_response.content)
                pictogram_data['svg_path'] = str(svg_file)
                
                # Obtener metadata para cada idioma
                for locale in locales:
                    try:
                        meta_url = f"{self.base_url}/pictograms/{pictogram_id}/{locale}"
                        meta_response = requests.get(meta_url)
                        metadata = meta_response.json()
                        
                        pictogram_data['translations'][locale] = {
                            'keyword': metadata.get('keyword'),
                            'meaning': metadata.get('meaning'),
                            'tags': metadata.get('tags', [])
                        }
                        
                        # Guardar metadata por idioma
                        metadata_file = self.output_dir / f"{pictogram_id}_{locale}.json"
                        with metadata_file.open('w') as f:
                            json.dump({
                                'source': 'arasaac',
                                'id': pictogram_id,
                                'locale': locale,
                                **pictogram_data['translations'][locale]
                            }, f)
                            
                    except Exception as e:
                        self.logger.error(f"Error con metadata {locale} para pictograma {pictogram_id}: {str(e)}")
                
                return pictogram_data
                
        except Exception as e:
            self.logger.error(f"Error descargando pictograma {pictogram_id}: {str(e)}")
            return {}
            
    def download_all(self, limit: Optional[int] = None) -> List[Dict]:
        """Descarga todos los pictogramas disponibles"""
        all_pictograms = []
        keywords = self.get_keywords()
        
        if limit:
            keywords = keywords[:limit]
            
        for keyword in keywords:
            try:
                pictogram = self.download_pictogram(keyword)
                if pictogram:
                    all_pictograms.append(pictogram)
            except Exception as e:
                self.logger.error(f"Error procesando keyword {keyword}: {str(e)}")
                continue
                
        return all_pictograms
