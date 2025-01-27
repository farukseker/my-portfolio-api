import logging
from typing import NoReturn
import psutil
from time import perf_counter
from colorlog import ColoredFormatter


log_format = (
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
)
formatter = ColoredFormatter(
    log_format,
    log_colors={
        "DEBUG": "white",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

file_handler = logging.FileHandler("performance.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)


def get_performance_metric(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        process = psutil.Process()
        start_memory = process.memory_info().rss / (1024 * 1024)

        try:
            return func(*args, **kwargs)
        except Exception as exception:
            logger.error("An error occurred in function (%s): %s", func.__name__, str(exception))
            raise exception
        finally:
            end_time = perf_counter()
            end_memory = process.memory_info().rss / (1024 * 1024)

            total_time = round(end_time - start_time, 2)
            memory_used = round(end_memory - start_memory, 2)

            log_message = (
                f"Process Time: {total_time} seconds | "
                f"Func Name: ({func.__name__}) | "
                f"Memory Used: {memory_used} MB"
            ).upper()

            if total_time > 10:
                logger.critical(log_message)
            elif 4 <= total_time <= 10:
                logger.warning(log_message)
            else:
                logger.info(log_message)

    return wrapper


if __name__ == '__main__':
    @get_performance_metric
    def example_function_short() -> NoReturn:
        sum(range(10**6))

    @get_performance_metric
    def example_function_medium() -> NoReturn:
        sum(range(10**7))


    @get_performance_metric
    def example_function_long() -> NoReturn:
        import time
        time.sleep(12)


    example_function_short()
    example_function_medium()
    example_function_long()
