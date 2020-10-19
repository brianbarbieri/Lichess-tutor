import os


class Config:
    with open("./secret.csv", "r") as r:
        data = [line.replace("\n","").split(",") for line in r.readlines()]
    username = data[0][1]
    token = data[1][1]
    WTF_CSRF_SECRET_KEY = data[2][1]
