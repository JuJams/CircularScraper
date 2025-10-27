import requests

url = 'https://example.com/data/products.json'  
headers = {
    'User-Agent': 'Mozilla/5.0',  
}

response = requests.get(url, headers=headers)
data = response.json()
print(data) 
