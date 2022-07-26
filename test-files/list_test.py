import requests

contacts_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/"

headers = {
    "Authorization" : "Token "
}

key = input("Enter API Token: ")
headers["Authorization"] += key

response = requests.get(contacts_url, headers=headers)

x = response.json()
print(len(x))
print(x)