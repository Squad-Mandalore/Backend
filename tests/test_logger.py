import os

from _pytest.logging import LogCaptureFixture
from fastapi.testclient import TestClient

from src.logger.logger import logger
from tests.define_test_variables import TestVariables, client_fixture, session_fixture


def test_logger_debug(caplog: LogCaptureFixture, client: TestClient) -> None:
    debug_message: str = "Spam and eggs are the same as eggs and spam."
    logger.debug(debug_message)
    for record in caplog.records:
        assert record.levelname == "DEBUG"
        assert debug_message in record.message

    caplog.clear()

    client.post("/log/debug", json={"message": debug_message}, headers=TestVariables.headers)
    for record in caplog.records:
        assert record.levelname == "DEBUG"
        assert debug_message in record.message

    caplog.clear()


def test_logger_info(caplog: LogCaptureFixture, client: TestClient) -> None:
    info_message: str = "Spam and eggs are a lot like eggs and spam."
    logger.info(info_message)
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert info_message in record.message

    caplog.clear()

    client.post("/log/info", json={"message": info_message}, headers=TestVariables.headers)
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert info_message in record.message

    caplog.clear()


def test_logger_warning(caplog: LogCaptureFixture, client: TestClient) -> None:
    warning_message: str = "Spam and eggs are not the same as eggs and spam."
    logger.warning(warning_message)
    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert warning_message in record.message

    caplog.clear()

    client.post("/log/warning", json={"message": warning_message}, headers=TestVariables.headers)
    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert warning_message in record.message

    caplog.clear()

def test_logger_critical(caplog: LogCaptureFixture, client: TestClient) -> None:
    critical_message: str = "Spam and eggs are plin plin plon."
    logger.critical(critical_message)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
        assert critical_message in record.message

    caplog.clear()

    client.post("/log/critical", json={"message": critical_message}, headers=TestVariables.headers)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
        assert critical_message in record.message

    caplog.clear()


def test_logger_error(caplog: LogCaptureFixture, client: TestClient) -> None:
    error_message: str = "Spam and eggs are 42"
    logger.error(error_message)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_message in record.message

    caplog.clear()

    client.post("/log/error", json={"message": error_message}, headers=TestVariables.headers)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_message in record.message

    caplog.clear()

def test_get_error_log(client: TestClient) -> None:
    # Remove error.log if it exists
    if os.path.exists("error.log"):
        os.remove("error.log")

    # Try to get error.log
    response = client.get("/log/error.log")
    assert response.status_code == 404

    # Create error.log
    with open("error.log", "w"): pass

    response = client.get("/log/error.log")
    assert response.status_code == 200

