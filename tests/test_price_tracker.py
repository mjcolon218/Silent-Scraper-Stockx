# tests/test_price_tracker.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from lambda_fn.pricetracker import lambda_handler

@patch('lambda_fn.pricetracker.fetch_sneaker_data', return_value=300.0)
@patch('lambda_fn.pricetracker.ses')
@patch('lambda_fn.pricetracker.table')
def test_lambda_handler_no_alert(mock_table, mock_ses, mock_fetch):
    mock_table.scan.return_value = {
        'Items': [{
            'sku': 'yeezy-boost-350',
            'name': 'Yeezy Boost 350',
            'target_price': 250.0
        }]
    }

    result = lambda_handler({}, {})
    
    mock_fetch.assert_called_once()
    mock_ses.send_email.assert_not_called()
    mock_table.update_item.assert_not_called()
    assert result['statusCode'] == 200
if __name__ == "__main__":
    test_lambda_handler_no_alert()  # Simulate an empty AWS event/context for local testing
