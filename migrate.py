#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from flask_migrate import Migrate


from app import app
from models.db import db, init_db

init_db()
migrate = Migrate(app, db)


