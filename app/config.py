class CoolConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://flask:password@localhost:5432/flask_sample"
    SQLALCHEMY_TRACK_MODIFICATIONS = False