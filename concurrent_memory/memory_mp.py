import multiprocessing
from functools import wraps


class MemorizeMP:
    """A class to cache the result of a function call in multiprocessing environment"""

    def __init__(self):
        self.manager = multiprocessing.Manager()

    def cache(self, func):
        memoization_cache = multiprocessing.Manager().dict()
        locks = multiprocessing.Manager().dict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))

            # Fast path to return the cached result if it exists
            if key in memoization_cache:
                print(f"key={key} found in cache")
                return memoization_cache[key]

            if key not in memoization_cache:
                # Create a new lock for the key if it doesn't exist
                locks[key] = self.manager.Lock()

            # Lock to ensure only 1 calculation is performed at a time
            with locks[key]:
                # Check again if the calculation is already done as other threads might have updated it
                if key not in memoization_cache:
                    # Perform the calculation and store the result in memoization_cache
                    memoization_cache[key] = func(*args, **kwargs)
            return memoization_cache[key]

        return wrapper
