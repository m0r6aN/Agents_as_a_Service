# agents_as_a_service/core/utils/retry_utils.py

import time
import logging

class Retry:
    @staticmethod
    def retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,)):
        """
        Decorator for retrying a function in case of specified exceptions.
        :param max_retries: Number of times to retry the function
        :param delay: Delay in seconds between retries
        :param exceptions: Tuple of exception types to catch and retry on
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                retries = 0
                while retries < max_retries:
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        retries += 1
                        logging.warning(f"Exception occurred: {e}. Retrying {retries}/{max_retries}...")
                        time.sleep(delay)
                raise Exception(f"Function failed after {max_retries} retries.")
            return wrapper
        return decorator
