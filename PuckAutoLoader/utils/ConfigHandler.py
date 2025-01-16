import os
import configparser

class ConfigHandler:
    def __init__(self, file):
        """
        configparser를 핸들링하기 위한 클래스
        :param file: 설정 파일 경로
        """
        self.loadConfig(file)
        self.file = file

    def loadConfig(self, file):
        if os.path.exists(file) == False:
            raise Exception('%s file does not exist. \n' %file)

        self.config = configparser.ConfigParser()
        self.config.read(file)

    def get_config(self):
        return self.config
