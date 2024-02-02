from tests.define_test_variables import TestVariables, client


def test_get_all_users() -> None:
    response = client.get(TestVariables.BASEURL + "/users/all")
    assert response.status_code == 200, str(response.status_code) + ": " + str(response.content)
    # assert response.json() == [{'id': 1, 'password': 'spam and eggs', 'username': 'user1'}]

# def test_get_user_by_id() -> None:
#     response = client.get(TestVariables.BASEURL + "/users/1")
#     assert response.status_code == 200, str(response.status_code) + ": " + str(response.content)
#     assert response.json() == {'id': 1, 'password': 'spam and eggs', 'username': 'user1'}
