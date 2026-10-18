import sys
import timeit
from pathlib import Path

# Let the script find customer_lookup.py in the src folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from customer_lookup import (
    customer_exists,
    build_customer_set,
    customer_exists_set,
    customer_exists_binary,
)

SIZES = [1_000, 10_000, 100_000, 1_000_000]
MISSING_ID = -1 # Never in the list, so every version hits its worst case.

def time_per_call(func, repeats):
    """Run func many times and return the average seconds per call."""
    total = timeit.timeit(func, number=repeats)
    return total / repeats

def main():
    print(f"{'Size':>10} {'Linear':>12} {'Built-in in':>12} {'Built set':>12} {'Set lookup':12} {'Binary':>12}")
    
    for size in SIZES:
        ids = list(range(size))
        ids =list(range(size))
        customer_set = build_customer_set(ids)
        
        linear = time_per_call(lambda: customer_exists(ids, MISSING_ID), repeats=10)
        built_in = time_per_call(lambda: MISSING_ID in ids, repeats=10)
        built = time_per_call(lambda: build_customer_set((ids)), repeats=10)
        set_lookup = time_per_call(lambda: customer_exists_set(customer_set, MISSING_ID), repeats=10_000)
        binary = time_per_call(lambda: customer_exists_binary(ids, MISSING_ID), repeats=10_000)
        
        print(
            f"{size:>10,} {linear * 1e6:>10.1f}µs {built_in * 1e6:>10.1f}µs "
            f"{built * 1e6:>10.1f}µs {set_lookup * 1e6:>10.3f}µs {binary * 1e6:>10.3f}µs"
        )
        
if __name__ == "__main__":
    main()