# migrate.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from flask_migrate import Migrate


import app
from app.models.db import db, init_db

init_db(app)
migrate = Migrate(app, db)


