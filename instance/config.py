class DevelopmentConfig:
    DEBUG = True
    ENV = 'development'


class TestingConfig:
    DEBUG = True


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}