# src/pictonet_data/collectors/openmoji.py
import json
import requests
from pathlib import Path
from typing import List, Dict
from .base import BaseDataCollector

class OpenMojiCollector(BaseDataCollector):
    def __init__(self, output_dir: str = "datasets/openmoji"):
        super().__init__(output_dir)
        self.base_url = "https://raw.githubusercontent.com/hfg-gmuend/openmoji"
        self.version = "14.0.0"
        self.metadata_url = f"{self.base_url}/{self.version}/data/openmoji.json"
    
    def download_all(self) -> List[Dict]:
        """Descarga todos los emojis de OpenMoji"""
        try:
            # Descargar metadata
            self.logger.info(f"Descargando metadata desde {self.metadata_url}")
            response = requests.get(self.metadata_url)
            metadata = response.json()
            
            processed_emojis = []
            for emoji in metadata:
                try:
                    # Descargar SVG
                    emoji_hex = emoji['hexcode']
                    svg_url = f"{self.base_url}/{self.version}/color/svg/{emoji_hex}.svg"
                    svg_response = requests.get(svg_url)
                    
                    if svg_response.status_code == 200:
                        # Guardar SVG
                        svg_file = self.output_dir / f"{emoji_hex}.svg"
                        svg_file.write_bytes(svg_response.content)
                        
                        # Guardar metadata
                        emoji_data = {
                            'source': 'openmoji',
                            'hexcode': emoji_hex,
                            'annotation': emoji['annotation'],
                            'tags': emoji['tags'],
                            'group': emoji['group'],
                            'subgroups': emoji['subgroups']
                        }
                        
                        metadata_file = self.output_dir / f"{emoji_hex}.json"
                        with open(metadata_file, 'w') as f:
                            json.dump(emoji_data, f)
                        
                        processed_emojis.append(emoji_data)
                        self.logger.info(f"Procesado emoji: {emoji['annotation']}")
                            
                except Exception as e:
                    self.logger.error(f"Error procesando emoji {emoji_hex}: {str(e)}")
                    continue
                
            return processed_emojis
                
        except Exception as e:
            self.logger.error(f"Error descargando OpenMoji: {str(e)}")
            return []