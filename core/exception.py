class ShadowException(Exception):
    pass

class InjectionError(ShadowException):
    pass

class TakeoverError(ShadowException):
    pass