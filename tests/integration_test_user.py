from tests.define_test_variables import TestVariables
import json


def test_login() -> None:

    # add a user
    # get the id of the user
    # login with the user
    response = requests.post(headers=TestVariables.HEADERS, json=data, url=TestVariables.BASEURL + "users/login")
    response_str = response.content.decode('utf-8')
    print(response_str)

    print("SECOND_CASE: PASSWORD SHOULD BE WRONG")
    data = '{"id": "' + str(id) + '", "password": "wrong_password"}'
    data = json.loads(data)
    response = requests.post(headers=TestVariables.HEADERS, json=data, url=TestVariables.BASEURL  + "users/login")
    response_str = response.content.decode('utf-8')
    print(response_str)

    print("THIRD_CASE: USER SHOULDNT BE FOUND")
    data = '{"id": "1", "password": "wrong_password"}'
    data = json.loads(data)
    response = requests.post(headers=TestVariables.HEADERS, json=data, url=TestVariables.BASEURL  + "users/login")
    response_str = response.content.decode('utf-8')
    print(response_str)


def testing_get_all() -> None:
    print("SHOULD RETURN ALL CURRENT USERS")
    response = requests.get(headers=TestVariables.HEADERS, url=TestVariables.BASEURL + "users/all")
    if response.status_code == 200:
        print("All current Users were returned")
    else:
        print(f"Error: {response.status_code}")
