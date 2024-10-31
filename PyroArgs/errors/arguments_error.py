# PyroArgs/errors/arguments_error.py
class ArgumentsError(Exception):
    __module__ = 'PyroArgs.errors'

    def __init__(self, message: str):
        super().__init__(message)
