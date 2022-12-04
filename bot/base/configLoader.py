import yaml


class LoadConfig:
    @classmethod
    def BotToken(cls, configFilePath):
        with open(configFilePath, 'r') as configFile:
            config = yaml.load(configFile, Loader=yaml.SafeLoader)
            return config['botToken']

    @classmethod
    def ownerId(cls, configFilePath):
        with open(configFilePath, 'r') as configFile:
            config = yaml.load(configFile, Loader=yaml.SafeLoader)
            return config['ownerId']