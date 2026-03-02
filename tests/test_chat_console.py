import pytest
from src.chat_console import process_order

def test_process_order():
    """Test processing an order by ID."""
    order_id = 123
    result = process_order(order_id)
    assert result == True
