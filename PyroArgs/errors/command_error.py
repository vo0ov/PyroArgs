# PyroArgs/errors/command_error.py
class CommandError(Exception):
    __module__ = 'PyroArgs.errors'

    def __init__(self, message: str):
        super().__init__(message)
