import pytest
from hypothesis import given, strategies as st
from customer_lookup import ( 
customer_exists, 
build_customer_set, 
customer_exists_set, 
customer_exists_binary,
)


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
        
# Test for binary search function
SORTED_IDS = (101, 202, 303, 404, 505, 606, 707,)


def test_binary_existing_id_returns_true():
    assert customer_exists_binary(SORTED_IDS, 606) is True
    
def test_binary_missing_id_returns_false():
    assert customer_exists_binary(SORTED_IDS, 808) is False
    
def test_binary_first_and_last_items_found():
    assert customer_exists_binary(SORTED_IDS, 101) is True
    assert customer_exists_binary(SORTED_IDS, 707) is True
    
def test_binary_empty_list_returns_false():
    assert customer_exists_binary([], 202) is False
    
def test_binary_binary_none_raises_type_error():
    with pytest.raises(TypeError):
        customer_exists_binary(None, 202)
        
def test_binary_unsorted_input_gives_wrong_answer():
    # 101 is in the list, but the list breaks the sorted contract.
    assert customer_exists_binary([303, 202, 101], 101) is False
    
@given(st.lists(st.integers()), st.integers())
def test_all_three_versions_agree(customer_ids, target_id):
    expected = customer_exists(customer_ids, target_id)
    
    customer_set = build_customer_set(customer_ids)
    assert customer_exists_set(customer_set, target_id) is expected
    
    sorted_ids = sorted(customer_ids)
    assert customer_exists_binary(sorted_ids, target_id) is expected
    