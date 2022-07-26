import requests

login_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/login/"

login_data = {
    "username": "",
    "password": ""
}

login_data["username"] = input("Enter username: ")
login_data["password"] = input("Enter password: ")

response = requests.post(login_url, data=login_data)

# print(response)
# print(response.content)
x = response.json()
print(type(x))
try:
    print(f"Your API Token is : {x['key']}")
except:
    print("Incorrect Password")