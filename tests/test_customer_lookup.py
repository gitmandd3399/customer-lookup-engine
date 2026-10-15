import pytest
from customer_lookup import customer_exists

def test_existing_id_returns_true():
    assert customer_exists([101, 202, 303], 202) is True
    
def test_missing_id_returns_false():
    assert customer_exists([101, 202, 303], 404) is False
    
def test_empty_list_returns_false():
    assert customer_exists([], 202) is False
    
def test_last_item_returns_true():
    assert customer_exists([101, 202, 303], 303) is True

def test_none_raises_type_error():
    with pytest.raises(TypeError):
        customer_exists(None, 202)        