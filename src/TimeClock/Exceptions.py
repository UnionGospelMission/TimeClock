class DatabasException(Exception):
    pass


class AccessException(Exception):
    pass


class InvalidTransformation(DatabasException):
    pass


class PermissionDenied(Exception): pass
