class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class dev_config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test_user:123456@localhost:3306/webide?charset=utf8mb4"
    DEBUG = True
    FLASK_ENV = 'development'


config = {'development': dev_config, 'default': dev_config}
