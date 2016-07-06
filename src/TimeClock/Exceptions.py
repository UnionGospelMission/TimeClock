class DatabasException(Exception):
    pass


class AccessException(Exception):
    pass


class InvalidTransformation(DatabasException):
    pass


class EventCancelled(Exception):
    pass


class DatabaseChangeCancelled(EventCancelled, DatabasException):
    pass


class PermissionDenied(Exception):
    pass


class ReportCancelled(EventCancelled):
    pass
