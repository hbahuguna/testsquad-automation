def test_process_order():
    """Test processing an order by ID."""
    result = process_order(123)
    assert result == True
