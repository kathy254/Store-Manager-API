class Config(object):
    #Parent configuration class
    DEBUG = False
    SECRET = '765uytjhgmnb'
    ENV='development'
    TESTING=False


class DevelopmentConfig(Config):
    #configurations for development
    DEBUG = True


class TestingConfig(Config):
    #Configurations for testing
    TESTING = True
    

class StagingConfig(Config):
    #Configurations for staging
    DEBUG = True


class ProductionConfig(Config):
    #Configurations for production
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
