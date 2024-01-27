import requests
import json

headers = {'content-type': 'application/json'}
url = 'http://127.0.0.1:8000/users'
id = 0
def testing_add_user():


    data = '{"password": "given_password"}'
    data = json.loads(data)
    response = requests.post(headers=headers, json=data, url=url + "/signup")
    if response.status_code == 201:
        # Convert bytes to string
        response_str = response.content.decode('utf-8')
        # Parse JSON
        response_dict = json.loads(response_str)
        # Extract the "id" field
        id_value = response_dict['id']
        print(f"User was created with following ID: {id_value}")
        global id
        id = id_value

    else:
        print(f"Error: {response.status_code}")

def testing_login():

    print("FIRST_CASE: PASSWORD SHOULD BE CORRECT")
    global id
    data = '{"id": "' + id + '", "password": "given_password"}'
    data = json.loads(data)
    response = requests.post(headers=headers, json=data, url=url + "/login")
    response_str = response.content.decode('utf-8')
    print(response_str)

    print("SECOND_CASE: PASSWORD SHOULD BE WRONG")
    data = '{"id": "' + id + '", "password": "wrong_password"}'
    data = json.loads(data)
    response = requests.post(headers=headers, json=data, url=url + "/login")
    response_str = response.content.decode('utf-8')
    print(response_str)

    print("THIRD_CASE: USER SHOULDNT BE FOUND")
    data = '{"id": "1", "password": "wrong_password"}'
    data = json.loads(data)
    response = requests.post(headers=headers, json=data, url=url + "/login")
    response_str = response.content.decode('utf-8')
    print(response_str)


def testing_get_all():
    print("SHOULD RETURN ALL CURRENT USERS")
    response = requests.get(headers=headers, url=url + "/all")
    if response.status_code == 200:
        print("All current Users were returned")
    else:
        print(f"Error: {response.status_code}")




testing_add_user()
testing_login()
testing_get_all()