import requests

headers ={
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzg2NjY0Nzg1fQ.4LMvMt-ZOAETMqnbkDdUwbJvq6tEJTSs41Xy95_xyrw"
}

re = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(re)
print(re.json)