class AnyPayAPIError(Exception):
    """
    Base AnyPay Exception.
    Exception codes and their meanings can be found here: https://anypay.io/doc/api/errors
    """

    def __init__(self, exception: dict):
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
