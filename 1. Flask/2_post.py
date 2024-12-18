import requests

url = 'http://localhost:5050/json/'
data = {
    'first_num': 12,
    'second_num': 25
}

response = requests.post(url, json=data)

print(response.json())  