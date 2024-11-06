# src/pictonet_data/processors/svg_cleaner.py
import re
from pathlib import Path
from typing import Union
from xml.etree import ElementTree as ET

class SVGCleaner:
    def __init__(self):
        self.namespaces = {
            'svg': 'http://www.w3.org/2000/svg'
        }
        
    def clean_svg(self, svg_path: Union[str, Path]) -> str:
        """Limpia y optimiza un archivo SVG"""
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Remover elementos innecesarios
        for elem in root.findall('.//svg:metadata', self.namespaces):
            root.remove(elem)
            
        # Normalizar viewBox
        if 'viewBox' not in root.attrib:
            width = root.attrib.get('width', '100')
            height = root.attrib.get('height', '100')
            root.attrib['viewBox'] = f"0 0 {width} {height}"
            
        # Convertir a string
        return ET.tostring(root, encoding='unicode')