import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.stockx_scraper import fetch_sneaker_data

def test_fetch_sneaker_data():
    data = fetch_sneaker_data("jordan 4")
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "price" in data[0]
    assert "link" in data[0]
print("Running test_fetch_sneaker_data...")
if __name__ == "__main__":
    test_fetch_sneaker_data()
    print("All tests passed!")