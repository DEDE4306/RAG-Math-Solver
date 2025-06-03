#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import requests



url = "http://127.0.0.1:5000/api/account/register"
data = {
    "phonenumber": "16789237652",
    "code": "168940",
    "username": "admin",
    "password": "password1",
}

print(os.listdir(".."))
file = r"..\static\avatars\1.png"
rec = requests.post(url, data=data, files={"avatar": open(file, "rb")})

print(rec.json())