# Customer Lookup Engine

Three ways to check whether a customer ID exists, benchmarked from 1,000 to 1,000,000 IDs, with tests proving all three always give the same answer.

I built this to practice the fundamentals behind a common interview question: you have a million customer IDs, so how do you check whether one exists, and what are the tradeoffs?

## What's inside

1. **Linear search** (`customer_exists`) walks the list one item at a time until it finds the target or runs out of items.
2. **Hash set** (`build_customer_set` and `customer_exists_set`) builds a set once, then checks it as many times as needed.
3. **Binary search** (`customer_exists_binary`) checks the middle of a sorted list and throws away the half that can't hold the target, until it finds it or nothing is left.

## Complexity

| Version | Time | Space | Notes |
| --- | --- | --- | --- |
| Linear search | O(n) | O(1) | Works on any list. Stops early if it finds a match. |
| Build the set | O(n) | O(n) | Paid once, up front. |
| Set lookup | O(1) average | None extra | Only fast after the set is built. |
| Binary search | O(log n) | O(1) | List must already be sorted. |

## Benchmark results

Every version searched for a missing ID, so each one hit its worst case. Times are microseconds per call, measured on my Mac with `timeit`.

| List size | Linear | Built-in `in` | Build set | Set lookup | Binary |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 8.0 | 3.0 | 4.6 | 0.035 | 0.624 |
| 10,000 | 70.4 | 28.5 | 45.1 | 0.034 | 0.834 |
| 100,000 | 615.5 | 269.1 | 485.1 | 0.033 | 0.965 |
| 1,000,000 | 8,905.4 | 8,800.6 | 8,726.7 | 0.034 | 1.316 |

What the numbers show:

1. **Linear search and building the set both grow about 10 times for every 10 times more data.** That's O(n).
2. **Set lookup stayed at about 0.034 microseconds at every size.** A thousand IDs or a million, it didn't matter. That's O(1).
3. **Binary search went from 0.6 to 1.3 microseconds across a thousand times more data.** Each 10x only adds about three more halvings. That's O(log n).
4. **Python's built-in `in` was about 2.5 times faster than my loop at small sizes, but grew at the same rate.** It's written in C, so each comparison is cheaper, but it still checks every item. Big O tells you how something grows, not how fast it is.

## When to use which

1. **One lookup, or a short list:** linear search. Building a set costs about the same as one linear search, so it doesn't pay off for a single check.
2. **Many lookups against the same data:** a hash set. The build costs about one linear search, so it pays for itself by the second lookup.
3. **Data that's already sorted, or memory is tight:** binary search. It's fast and needs no extra memory, but if the data isn't sorted, sorting first costs O(n log n).

## Design decisions

1. **The set version is split into two functions.** If the lookup built the set every call, each call would cost O(n), which is no better than linear search. Splitting it makes build-once, look-up-many the default.
2. **Binary search doesn't check whether the list is sorted.** Checking would cost O(n) and wipe out the speed advantage. Instead, the docstring states the contract, and a test documents what happens when it's broken: wrong answers, not errors.
3. **Empty lists return `False`, and `None` raises a `TypeError`.** An empty list is valid input with nothing in it. `None` usually means something went wrong upstream, so the code fails loudly instead of hiding it.
4. **Duplicates are allowed.** None of the three versions needs unique IDs to give the right answer.

## Testing

There are 17 tests:

1. **Example tests for each version:** an existing ID, a missing ID, an empty list, the last item, duplicates, and `None`.
2. **A test documenting the sorted contract:** binary search on `[303, 202, 101]` misses 101, which is in the list.
3. **A property-based test using Hypothesis:** it generates random lists and targets, about 100 cases per run, and checks that all three versions always agree with linear search.

When I passed unsorted data to binary search on purpose, Hypothesis found and shrank the failure to the smallest case possible: searching `[1, 0]` for `0`. I didn't have to think of that case myself.

## Running it

```bash
git clone https://github.com/gitmandd3399/customer-lookup-engine.git
cd customer-lookup-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
python benchmarks/benchmark_lookup.py
```

The benchmark takes about 10 seconds.

## Project structure

```
customer-lookup-engine/
├── src/customer_lookup.py          # The three implementations
├── tests/test_customer_lookup.py   # Example tests and the Hypothesis test
├── benchmarks/benchmark_lookup.py  # The timeit benchmark
├── pyproject.toml                  # Tells pytest where the code lives
└── requirements.txt                # pytest and hypothesis
```
