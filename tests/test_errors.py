# tests/test_errors.py
import pytest
from unittest.mock import MagicMock
from PyroArgs.errors.arguments_error import ArgumentsError
from PyroArgs.errors.command_error import CommandError
from PyroArgs.errors.permissions_error import PermissionsError


@pytest.fixture
def sample_message():
    return "Sample message"


def test_arguments_error():
    mock_message = MagicMock()
    mock_message.from_user.username = "testuser"

    error = ArgumentsError(
        command="test_command",
        message=mock_message,
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        missing_arg="arg2",
        arg_position=2
    )
    assert isinstance(error, Exception)
    assert "ArgumentsError: Missing required argument" in str(error)
    assert error.command == "test_command"
    assert error.message == mock_message
    assert error.parsed_args == ["arg1"]
    assert error.parsed_kwargs == {"key1": "value1"}
    assert error.missing_arg == "arg2"
    assert error.arg_position == 2


def test_command_error():
    error = CommandError(
        command="test_command",
        message="Sample message",
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        error_message="An error occurred"
    )
    assert isinstance(error, Exception)
    assert "Command error: Error in command" in str(error)
    assert error.command == "test_command"
    assert error.message == "Sample message"
    assert error.parsed_args == ["arg1"]
    assert error.parsed_kwargs == {"key1": "value1"}
    assert error.error_message == "An error occurred"


def test_permissions_error():
    error = PermissionsError(
        command="test_command",
        message="Sample message",
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"}
    )
    assert isinstance(error, Exception)
    assert "Permissions error: User does not have permission" in str(error)
    assert error.command == "test_command"
    assert error.message == "Sample message"
    assert error.parsed_args == ["arg1"]
    assert error.parsed_kwargs == {"key1": "value1"}
