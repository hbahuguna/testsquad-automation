import pytest
from src.human_prompt_manager import process_order

def test_process_order():
    """Test processing an order by ID."""
    order_id = "12345"
    result = process_order(order_id)
    assert result == True
