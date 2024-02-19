from src.logger.logger import logger
from tests.define_test_variables import client, TestVariables
from _pytest.logging import LogCaptureFixture


def test_logger_debug(caplog: LogCaptureFixture) -> None:
    debug_message: str = "Spam and eggs are the same as eggs and spam."
    logger.debug(debug_message)
    for record in caplog.records:
        assert record.levelname == "DEBUG"
        assert debug_message in record.message

    caplog.clear()

    client.post(TestVariables.BASEURL + "/log/debug", json={"message": debug_message}, headers=TestVariables.HEADERS)
    for record in caplog.records:
        assert record.levelname == "DEBUG"
        assert debug_message in record.message

    caplog.clear()


def test_logger_info(caplog: LogCaptureFixture) -> None:
    info_message: str = "Spam and eggs are a lot like eggs and spam."
    logger.info(info_message)
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert info_message in record.message

    caplog.clear()

    client.post(TestVariables.BASEURL + "/log/info", json={"message": info_message}, headers=TestVariables.HEADERS)
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert info_message in record.message

    caplog.clear()


def test_logger_warning(caplog: LogCaptureFixture) -> None:
    warning_message: str = "Spam and eggs are not the same as eggs and spam."
    logger.warning(warning_message)
    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert warning_message in record.message

    caplog.clear()

    client.post(TestVariables.BASEURL + "/log/warning", json={"message": warning_message}, headers=TestVariables.HEADERS)
    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert warning_message in record.message

    caplog.clear()

def test_logger_critical(caplog: LogCaptureFixture) -> None:
    critical_message: str = "Spam and eggs are plin plin plon."
    logger.critical(critical_message)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
        assert critical_message in record.message

    caplog.clear()

    client.post(TestVariables.BASEURL + "/log/critical", json={"message": critical_message}, headers=TestVariables.HEADERS)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
        assert critical_message in record.message

    caplog.clear()


def test_logger_error(caplog: LogCaptureFixture) -> None:
    error_message: str = "Spam and eggs are 42"
    logger.error(error_message)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_message in record.message

    caplog.clear()

    client.post(TestVariables.BASEURL + "/log/error", json={"message": error_message}, headers=TestVariables.HEADERS)
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_message in record.message

    caplog.clear()


def test_get_whoami(caplog: LogCaptureFixture) -> None:
    response = client.get(TestVariables.BASEURL + "/users/whoami", headers=TestVariables.HEADERS)
    assert response.status_code == 200

    for record in caplog.records:
        assert record.levelname == "WARNING"
        assert "Hey everybody take a look at me, my output lacks credibility!" in record.message

    caplog.clear()


def test_get_error_log() -> None:
    response = client.get(TestVariables.BASEURL + "/log/error.log")
    assert response.status_code == 200

