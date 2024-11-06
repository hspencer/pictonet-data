# tests/test_collectors.py
import pytest
from pictonet_data.collectors import QuickDrawCollector, OpenMojiCollector, ArasaacCollector

def test_quickdraw_collector():
    collector = QuickDrawCollector()
    categories = collector.get_categories()
    assert len(categories) > 0
    assert isinstance(categories, list)
    assert all(isinstance(c, str) for c in categories)

def test_openmoji_collector():
    collector = OpenMojiCollector()
    result = collector.download_all()
    assert isinstance(result, list)
    assert all('hexcode' in item for item in result)

def test_arasaac_collector():
    collector = ArasaacCollector()
    keywords = collector.get_keywords()
    assert len(keywords) > 0
    assert isinstance(keywords, list)