from datetime import date
from datetime import timedelta
import os
from unittest.mock import call
from unittest.mock import mock_open
from unittest.mock import patch

from _pytest.logging import LogCaptureFixture
from fastapi.testclient import TestClient
import pytest
from src.logger.logger import logger
from src.services.logger_service import check_log_age
from src.services.logger_service import clear_error_log
from src.services.logger_service import is_date_at_least_three_days_old

from tests.define_test_variables import TestVariables


def test_logger_debug(caplog: LogCaptureFixture, client: TestClient) -> None:
    debug_message: str = 'Spam and eggs are the same as eggs and spam.'
    logger.debug(debug_message)
    for record in caplog.records:
        assert record.levelname == 'DEBUG'
        assert debug_message in record.message

    caplog.clear()

    client.post(
        '/log/debug', json={'message': debug_message}, headers=TestVariables.headers
    )
    for record in caplog.records:
        assert record.levelname == 'DEBUG'
        assert debug_message in record.message

    caplog.clear()


def test_logger_info(caplog: LogCaptureFixture, client: TestClient) -> None:
    info_message: str = 'Spam and eggs are a lot like eggs and spam.'
    logger.info(info_message)
    for record in caplog.records:
        assert record.levelname == 'INFO'
        assert info_message in record.message

    caplog.clear()

    client.post(
        '/log/info', json={'message': info_message}, headers=TestVariables.headers
    )
    for record in caplog.records:
        assert record.levelname == 'INFO'
        assert info_message in record.message

    caplog.clear()


def test_logger_warning(caplog: LogCaptureFixture, client: TestClient) -> None:
    warning_message: str = 'Spam and eggs are not the same as eggs and spam.'
    logger.warning(warning_message)
    for record in caplog.records:
        assert record.levelname == 'WARNING'
        assert warning_message in record.message

    caplog.clear()

    client.post(
        '/log/warning', json={'message': warning_message}, headers=TestVariables.headers
    )
    for record in caplog.records:
        assert record.levelname == 'WARNING'
        assert warning_message in record.message

    caplog.clear()


def test_logger_critical(caplog: LogCaptureFixture, client: TestClient) -> None:
    critical_message: str = 'Spam and eggs are plin plin plon.'
    logger.critical(critical_message)
    for record in caplog.records:
        assert record.levelname == 'CRITICAL'
        assert critical_message in record.message

    caplog.clear()

    client.post(
        '/log/critical',
        json={'message': critical_message},
        headers=TestVariables.headers,
    )
    for record in caplog.records:
        assert record.levelname == 'CRITICAL'
        assert critical_message in record.message

    caplog.clear()


def test_logger_error(caplog: LogCaptureFixture, client: TestClient) -> None:
    error_message: str = 'Spam and eggs are 42'
    logger.error(error_message)
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert error_message in record.message

    caplog.clear()

    client.post(
        '/log/error', json={'message': error_message}, headers=TestVariables.headers
    )
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert error_message in record.message

    caplog.clear()


def test_get_error_log(client: TestClient) -> None:
    # Remove error.log if it exists
    if os.path.exists('./volume/error.log'):
        os.remove('./volume/error.log')

    # Try to get error.log
    response = client.get('/log/error.log')
    assert response.status_code == 404

    # Create error.log
    with open('./volume/error.log', 'w'):
        pass

    response = client.get('/log/error.log')
    assert response.status_code == 200


# Sample date string for tests
date_string = '2023-04-20'


@pytest.fixture
def mock_file():
    return mock_open(read_data=date_string)


@pytest.mark.parametrize(
    'test_date, expected',
    [
        (date(2023, 4, 17), True),
        (date(2023, 4, 19), True),
        (date.today() + timedelta(1), False),
    ],
)
def test_is_date_at_least_three_days_old(test_date, expected):
    assert is_date_at_least_three_days_old(test_date) == expected


def test_check_log_age(mock_file):
    with (
        patch('builtins.open', mock_file),
        patch('src.services.logger_service.os.path.getsize', return_value=1),
    ):
        assert check_log_age() == date(2023, 4, 20)


def test_check_log_age_failure(mock_file):
    mock_file.return_value.read = lambda x: ''  # Simulate end of file or error
    with (
        patch('builtins.open', mock_file),
        patch('src.services.logger_service.os.path.getsize', return_value=1),
        patch.object(logger, 'warning') as mock_warning,
    ):
        assert check_log_age() is None
        mock_warning.assert_called()


@pytest.mark.asyncio
async def test_clear_error_log_no_clear_needed():
    m = mock_open()
    with (
        patch('builtins.open', m),
        patch(
            'src.services.logger_service.check_log_age', return_value=date(2023, 4, 20)
        ),
        patch(
            'src.services.logger_service.is_date_at_least_three_days_old',
            return_value=False,
        ),
    ):
        await clear_error_log()
        assert call('./volume/error.log', 'w', encoding='utf-8') not in m.mock_calls


@pytest.mark.asyncio
async def test_clear_error_log_clear_needed():
    m = mock_open()
    with (
        patch('builtins.open', m),
        patch(
            'src.services.logger_service.check_log_age', return_value=date(2023, 4, 17)
        ),
        patch(
            'src.services.logger_service.is_date_at_least_three_days_old',
            return_value=True,
        ),
    ):
        await clear_error_log()
        assert call('./volume/error.log', 'w', encoding='utf-8') in m.mock_calls
