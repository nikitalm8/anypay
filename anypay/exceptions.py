from functools import wraps
from typing import Callable, Awaitable


class AnyPayAPIError(Exception):
    """
    Base AnyPay Exception.
    """
    
    def __init__(self, exception: dict) -> None:
        """
        AnyPay API Exception.
        
        :param exception: Exception data.
        
        :raises: AnyPayAPIError
        """

        self.message = exception['message']
        self.code = exception['code']

        super().__init__(
            '[%(code)s] AnyPayAPI Error: %(message)s' % exception,
        )


def error_check(func: Callable) -> Callable:

    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:

        response = func(self, *args, **kwargs)

        if 'error' in response:

            raise AnyPayAPIError(response['error'])

        return response

    return wrapper


def error_check_async(func: Awaitable) -> Awaitable:

    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> dict:

        response = await func(self, *args, **kwargs)

        if 'error' in response:

            raise AnyPayAPIError(response['error'])

        return response

    return wrapper
