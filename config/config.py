class DevelopmentConfigs(object):
    SECRET_KEY = 'mybuzzbreakapp'
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:Jeddac401@127.0.0.1:5432/buzzbreak"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pool_size = 32
    max_overflow = 64
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'hadipartiv21@gmail.com'
    MAIL_PASSWORD = 'lkgamqggscqkitnn'