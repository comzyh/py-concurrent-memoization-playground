import multiprocessing
import time

from .memory_mp import MemorizeMP

mmp = MemorizeMP()


@mmp.cache
def perform_calculation(key: int) -> int:
    "A calculation function that takes few seconds to complete"
    print(f"key={key}")
    time.sleep(2)
    return key * 2


if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor

    executor = ProcessPoolExecutor(2)

    for res in executor.map(
        perform_calculation, [1, 2, 1, 5, 3, 3, 3, 2, 4, 4, 4, 5, 5, 5, 5, 5, 5]
    ):
        pass
    perform_calculation(key=1)
