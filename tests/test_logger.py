# tests/test_logger.py
import pytest
from PyroArgs.types.message import Message
from unittest.mock import AsyncMock, MagicMock, patch
from PyroArgs.types.logger import Logger
from PyroArgs.errors.arguments_error import ArgumentsError
from PyroArgs.errors.command_error import CommandError
from PyroArgs.errors.permissions_error import PermissionsError


@pytest.fixture
def logger():
    return Logger()


@pytest.mark.asyncio
async def test_trigger_use_command(logger):
    logger.use_command = '{user} used {command} with args {args} and kwargs {kwargs}'
    mock_logger_info = AsyncMock()
    logger.logger.info = mock_logger_info

    with patch.object(logger, '_Logger__get_username', return_value='@testuser'):
        await logger.trigger_use_command(
            message="Test message",
            command="start",
            args=["arg1"],
            kwargs={"key1": "value1"}
        )
        mock_logger_info.assert_called_once_with(
            '@testuser used start with args [\'arg1\'] and kwargs {\'key1\': \'value1\'}'
        )


@pytest.mark.asyncio
async def test_trigger_arguments_error(logger):
    logger.arguments_error = '{user} failed to use {command} due to missing {missing_arg} at position {arg_position}'
    mock_logger_info = AsyncMock()
    logger.logger.info = mock_logger_info

    message = "Test message"
    error = ArgumentsError(
        command="start",
        message=message,
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        missing_arg="arg2",
        arg_position=2
    )

    with patch.object(logger, '_Logger__get_username', return_value='@testuser'):
        await logger.trigger_arguments_error(error)
        mock_logger_info.assert_called_once_with(
            '@testuser failed to use start due to missing arg2 at position 2'
        )


@pytest.mark.asyncio
async def test_trigger_command_error(logger):
    logger.command_error = '{user} encountered an error in {command}: {error}'
    mock_logger_info = AsyncMock()
    logger.logger.info = mock_logger_info

    message = "Test message"
    error = CommandError(
        command="start",
        message=message,
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"},
        error_message="An unexpected error"
    )

    with patch.object(logger, '_Logger__get_username', return_value='@testuser'):
        await logger.trigger_command_error(error)
        mock_logger_info.assert_called_once_with(
            '@testuser encountered an error in start: An unexpected error'
        )


@pytest.mark.asyncio
async def test_trigger_permissions_error(logger):
    logger.set_permissions_error(
        '{user} does not have permissions to use {command}')
    mock_logger_info = AsyncMock()
    logger.logger.info = mock_logger_info

    # Создаем мокированный объект Message с атрибутом from_user
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_message = MagicMock(spec=Message)
    mock_message.from_user = mock_user

    error = PermissionsError(
        command="start",
        message=mock_message,
        parsed_args=["arg1"],
        parsed_kwargs={"key1": "value1"}
    )

    with patch.object(logger, '_Logger__get_username', return_value='@testuser'):
        await logger.trigger_permissions_error(error)
        mock_logger_info.assert_called_once_with(
            '@testuser does not have permissions to use start'
        )
