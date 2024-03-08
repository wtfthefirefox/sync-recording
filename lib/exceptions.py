class AuthenticationError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class RequestParamsError(Exception):
    pass


class CommandExecutionError(Exception):
    pass


class BadGatewayError(Exception):
    pass

class NotFoundError(Exception):
    pass
