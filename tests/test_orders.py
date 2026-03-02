import pytest
from src.orders import process_order

def test_process_order():
    """Test processing an order."""
    order_id = "12345"
    result = process_order(order_id)
    assert result is True
