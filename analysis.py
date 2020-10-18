import requests
import json, ndjson

with open("secret.csv", "r") as r:
    data = [line.replace("\n","").split(",") for line in r.readlines()]
    username = data[0][1]
    token = data[1][1]

url = "https://lichess.org"
response = requests.get(
  f'https://lichess.org/api/games/user/{username}',
  params={
    "perfType" : "blitz",
  },
  headers={
    'Authorization': f'Bearer {token}', # Need this or you will get a 401: Not Authorized response
    "Accept": "application/x-ndjson"
  }
)

# Parse application/x-ndjson into list of JSON objects
resp_json = []
ndjson = response.content.decode().split('\n')

for json_obj in ndjson:
    if json_obj:
        resp_json.append(json.loads(json_obj))