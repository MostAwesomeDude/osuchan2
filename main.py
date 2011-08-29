#!/usr/bin/env python

if __name__ == "__main__":
    from main import app
    app.run(debug=True, host="0.0.0.0", port=1337)

import os

from flask import Flask

from osuchan.blueprint import osuchan
from osuchan.models import db

wd = os.getcwd()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s/test.db" % wd
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.urandom(16)
db.init_app(app)
app.register_blueprint(osuchan)
