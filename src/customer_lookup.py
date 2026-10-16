def customer_exists(customer_ids, target_id):
    """Return True if target_id appears in customer_ids, False otherwise.
    
    Args:
        customer_ids: A list of customer IDs, each an int.
        target_id: The customer ID to search for, an int.
        
    Returns:
        True if target_id is found at least once, False if it is not.
        
    Edge cases:
        An empty list returns False.
        Duplicate IDs are allowed and do not change the result.
        If customer_ids is None, a TypeError is raised.
    """
    for customer_id in customer_ids:
        if customer_id == target_id:
            return True
    return False

def build_customer_set(customer_ids):
    """Return a set containing every unique ID in customer_ids."""
    return set(customer_ids)

def customer_exists_set(customer_set, target_id):
    """Return True if target_id is in customer_set, False otherwise."""
    return target_id in customer_set


