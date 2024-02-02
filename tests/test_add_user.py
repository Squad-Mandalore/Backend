import json
import requests
from requests import Response
from tests.define_test_variables import TestVariables


def add_user(body: str = TestVariables.EXAMPLE_PASSWORD) -> Response:
    response = requests.post(headers=TestVariables.HEADERS, json=json.loads(body), url=TestVariables.BASEURL + "/users/signup")
    return response


# also test the password validation
def test_add_user() -> None:
    # first case - password should be correct
    password = '{"password": "spam and eggs"}'
    response = add_user(password)
    assert response.status_code == 201, str(response.status_code) + ": " + str(response.content)

    # second case - password should be incorrect
    password = '{"password": "spam"}'
    response = add_user(password)
    assert response.status_code == 400, str(response.status_code) + ": " + str(response.content)

    # third case - password are UTF-8 characters
    password = '{"password": "späm🥫🥫🥫 and ëggs🥚🥚🥚"}'
    response = add_user(password)
    assert response.status_code == 201, str(response.status_code) + ": " + str(response.content)
