#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests



url = "http://127.0.0.1:5000/api/account/loginWithPassword"
data = {
    "phonenumber": "15150793241",
    "password": "password1",
}

rec = requests.post(url, json=data)

print(rec.json())
