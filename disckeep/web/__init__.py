from disckeep.config.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from disckeep.web.models import Group, ReleaseGroup, ReleaseGroupType  # noqa: E402,F401

db.create_all()

from disckeep.web import routes  # noqa: E402,F401
