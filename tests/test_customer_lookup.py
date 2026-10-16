import pytest
from customer_lookup import customer_exists
from customer_lookup import customer_exists, build_customer_set, customer_exists_set

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
        #test 2
def test_set_existing_id_returns_true():
    customer_set = build_customer_set([101, 202, 303])
    assert customer_exists_set(customer_set, 303) is True


def test_set_missing_id_returns_false():
    customer_set = build_customer_set([101, 202, 303])
    assert customer_exists_set(customer_set, 404) is False


def test_set_empty_list_returns_false():
    customer_set = build_customer_set([])
    assert customer_exists_set(customer_set, 202) is False


def test_set_duplicates_still_found():
    customer_set = build_customer_set([101, 202, 202, 303])
    assert customer_exists_set(customer_set, 202) is True


def test_set_none_raises_type_error():
    with pytest.raises(TypeError):
        build_customer_set(None)