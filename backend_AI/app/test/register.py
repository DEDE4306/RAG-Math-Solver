#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from pathlib import Path
import os



url = "http://127.0.0.1:5000/api/account/register"
data = {
    "phonenumber": "16789237652",
    "code": "955135",
    "username": "admin",
    "password": "password1",
}
root_dir = Path(__file__).parent.parent
file = os.path.join(root_dir, "static","avatars","1.png")
rec = requests.post(url, data=data, files={"avatar": open(file, "rb")})

# print(rec.json())