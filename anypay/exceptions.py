from functools import wraps
from typing import Callable, Awaitable


class AnyPayAPIError(Exception):
    """
    Base AnyPay Exception.
    Exception codes and their meanings can be found here: https://anypay.io/doc/api/errors
    """
    
    def __init__(self, exception: dict) -> None:
        """
        AnyPay API Exception.
        Docs: https://anypay.io/doc/api/errors
        
        :param exception: Exception data (code and message).
        
        :raises: AnyPayAPIError
        """

        self.message = exception['message']
        self.code = exception['code']

        super().__init__(
            '[%(code)s] AnyPayAPI Error: %(message)s' % exception,
        )


def error_check(func: Callable) -> Callable:
    """
    Decorator for checking errors in response of sync methods.
    If there is an `error` key in the response, raises an AnyPayAPIError.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:

        response = func(self, *args, **kwargs)

        if 'error' in response:

            raise AnyPayAPIError(response['error'])

        return response

    return wrapper


def error_check_async(func: Awaitable) -> Awaitable:
    """
    Decorator for checking errors in response of async methods.
    If there is an `error` key in the response, raises an AnyPayAPIError.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> dict:

        response = await func(self, *args, **kwargs)

        if 'error' in response:

            raise AnyPayAPIError(response['error'])

        return response

    return wrapper
