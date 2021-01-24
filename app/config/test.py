import os


class Config:
    DEBUG = True

    # 分页配置
    COUNT_DEFAULT = 10
    PAGE_DEFAULT = 0

    # sqlalchemy
    # 屏蔽 sql alchemy 的 FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL')
    SQLALCHEMY_ECHO = False
    SECRET_KEY = '123456'

    # 中文不乱码
    JSON_AS_ASCII = False

    # Log
    LOG = True

    LOG_LEVEL = 'INFO'
    LOG_DIR = 'logs'
    LOG_SIZE_LIMIT = 1024 * 1024 * 5
    LOG_ENABLE_REQUEST_LOG = True
    LOG_FILE = True
