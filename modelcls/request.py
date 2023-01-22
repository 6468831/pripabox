import requests


url = "http://127.0.0.1:8000/predict"


files = {'image': open('2022-08-02 11_11_17-Smartphone Apple iPhone 11 128GB Black _ Public.png', 'rb')}
r = requests.post(url, files=files)

print(r.content)
