import time
import logging
from functools import wraps

class Retry:
    @staticmethod
    def retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,)):
        """
        Decorator to retry a function on specified exceptions.
        
        :param max_retries: Maximum number of retries before giving up.
        :param delay: Delay between retries in seconds.
        :param exceptions: Tuple of exceptions to catch and retry on.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                while retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        logging.error(f"Error in {func.__name__}: {e}. Retrying {retries + 1}/{max_retries}...")
                        retries += 1
                        time.sleep(delay)
                return func(*args, **kwargs)  # Last attempt without retry
            return wrapper
        return decorator
