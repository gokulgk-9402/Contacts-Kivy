import requests

details_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/1/"

headers = {
    "Authorization" : "Token "
}

key = input("Enter API Token: ")
headers["Authorization"] += key

response = requests.get(details_url, headers=headers)

x = response.json()
print(x)
