import multiprocessing
import time

from .memory_mp import MemorizeMP

mmp = MemorizeMP()

mp_manager = multiprocessing.Manager()
memoization_cache = mp_manager.dict()
locks = mp_manager.dict()

@mmp.cache
def perform_calculation(key)-> None:
    print(f"key={key}")
    time.sleep(5)
    
def memoized_calculation(key):
    
    # Fast path to return the cached result if it exists
    if key in memoization_cache:
        return memoization_cache[key]


    if key not in memoization_cache:
        # Create a new lock for the key if it doesn't exist
        locks[key] = mp_manager.Lock()

    # Lock to ensure only 1 calculation is performed at a time
    with locks[key]:
        # Check again if the calculation is already done as other threads might have updated it
        if key not in memoization_cache:
            # Perform the calculation and store the result in memoization_cache
            memoization_cache[key] = perform_calculation(key)
    return memoization_cache[key]


if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor

    executor = ProcessPoolExecutor(2)

    for res in executor.map(perform_calculation, [1,2,1,5,3,3,3,2,4,4,4,5,5,5,5,5,5]):
        pass