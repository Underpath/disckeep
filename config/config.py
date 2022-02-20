import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "my secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "disckeep.sqlite")
    # print("***")
    # print(SQLALCHEMY_DATABASE_URI)
    # print("***")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
