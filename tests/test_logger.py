import os
from src.logger.logger import logger
from tests.define_test_variables import client, TestVariables

def test_logger(caplog):
    logger.warning("Spam and eggs are not the same as eggs and spam.")
    assert "Spam and eggs are not the same as eggs and spam." in caplog.text

def test_get_whoami(caplog):
    response = client.get(TestVariables.BASEURL + "/users/whoami", headers=TestVariables.HEADERS)
    assert response.status_code == 200
    assert "Hey everybody take a look at me, my output lacks credibility!" in caplog.text
