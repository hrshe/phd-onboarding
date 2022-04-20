from pathlib import Path
from pipeline.base_logger import logger
import configparser

config = configparser.ConfigParser()

class Utilities:
    def __init__(self):
        self.root_dir_path = str(Path(__file__).parent.parent.parent.absolute())
        self.resources_dir_path = self.root_dir_path + '/resources'
        self.config_file_path = self.resources_dir_path + '/config.properties'
        self.measurement_set_path = None

        config.read(self.config_file_path)
        self.speed_of_light = float(config['general']['speed_of_light'])


    def get_root_dir_path(self):
        return self.root_dir_path

    def get_resources_dir_path(self):
        return self.resources_dir_path

    def get_measurement_set_path(self):
        return self.measurement_set_path

    def set_measurement_set_path(self, filename):
        self.measurement_set_path = self.resources_dir_path + '/' + filename  # todo - to be set from config file
        logger.debug(f"measurement set file path set as: {self.measurement_set_path}")
