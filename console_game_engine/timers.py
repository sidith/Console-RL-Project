import logging
from time import perf_counter

import yaml


def setup_logging():
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger('bechmark')


def benchmark(func):

    benchmark_logger = setup_logging()

    def wrapper(*args, **kwargs):
        func_name = func.__name__

        benchmark_logger.debug("~"*80)
        benchmark_logger.debug(f"Starting function {func_name}...")
        benchmark_logger.debug("~"*80)

        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_time = end_time - start_time

        benchmark_logger.debug("~"*80)
        benchmark_logger.debug(
            f"Function {func_name} took {elapsed_time:.4f} seconds to execute.")
        benchmark_logger.debug("~"*80)

        return result
    return wrapper
