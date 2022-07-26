import requests

register_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/registration/"

user_data = {
    "username": "",
    "email": "",
    "password1": "",
    "password2": ""
}
user_data["username"] = input("Enter username: ")
user_data["email"] = input("Enter email: ")
user_data["password1"] = input("Enter password: ")
user_data["password2"] = input("Confirm password: ")


response = requests.post(register_url, data=user_data)

# print(response)
# print(response.content)
x = response.json()
try:
    print(x['key'])
except:
    print("Unable to register!")