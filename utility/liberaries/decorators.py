# this file contains decorators for use in the mobile testing framework
import functools
import logging
import time
from typing import Callable, Any
from selenium.common.exceptions import WebDriverException
logger = logging.getLogger(__name__)

def retry_on_exception(
    exceptions: tuple = (WebDriverException,),
    attempts: int = 3,
    delay: float = 0.5,
) -> Callable:
    """
    Decorator to retry a function if specified exceptions are raised.

    :param exceptions: Tuple of exception classes to catch and retry on.
    :param attempts: Number of attempts before giving up.
    :param delay: Delay in seconds between attempts.
    :return: Decorated function with retry logic.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed with exception: {e}. Retrying after {delay} seconds...")
                    time.sleep(delay)
            logger.error(f"All {attempts} attempts failed. Raising last exception.")
            raise last_exception
        return wrapper
    return decorator

def log_function_call(func: Callable) -> Callable:
    """
    Decorator to log function calls with arguments and return values.

    :param func: Function to be decorated.
    :return: Decorated function with logging.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Calling function '{func.__name__}' with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"Function '{func.__name__}' returned: {result}")
        return result
    return wrapper

def time_function_execution(func: Callable) -> Callable:
    """
    Decorator to time the execution of a function.

    :param func: Function to be decorated.
    :return: Decorated function with timing.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

def suppress_exceptions(
    exceptions: tuple = (Exception,),
) -> Callable:
    """
    Decorator to suppress specified exceptions raised by a function.

    :param exceptions: Tuple of exception classes to suppress.
    :return: Decorated function that suppresses specified exceptions.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.warning(f"Suppressed exception in function '{func.__name__}': {e}")
                return None
        return wrapper
    return decorator


def ensure_return_type(
    return_type: type,
) -> Callable:
    """
    Decorator to ensure the return type of a function.

    :param return_type: Expected return type of the function.
    :return: Decorated function that checks return type.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            if not isinstance(result, return_type):
                raise TypeError(f"Function '{func.__name__}' returned type {type(result).__name__}, expected {return_type.__name__}")
            return result
        return wrapper
    return decorator
