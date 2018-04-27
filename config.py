import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    # RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() in \
    #     ['false', 'on', '0']
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in \
    #     ['false', 'on', '0']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    WEBMARK_MAIL_SUBJECT_PREFIX = '[WEBMARK]'
    WEBMARK_MAIL_SENDER = os.environ.get('WEBMARK_MAIL_SENDER')
    WEBMARK_ADMIN = os.environ.get('WEBMARK_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    WEBMARK_POSTS_PER_PAGE = 6
    WEBMARK_SCORES_PER_PAGE = 10
    WEBMARK_FOLLOWERS_PER_PAGE = 10
    WEBMARK_COMMENTS_PER_PAGE = 5
    WEBMARK_SLOW_DB_QUERY_TIME = 0.5
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
