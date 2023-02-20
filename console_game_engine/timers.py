from time import perf_counter


def print_fuction_duration(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        print(f"{func_name} took {end_time - start_time:.6e} seconds to run")
        return result
    return wrapper
