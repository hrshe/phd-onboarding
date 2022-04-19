from pathlib import Path


class Utilities:
    def __init__(self):
        self.root_dir_path = str(Path(__file__).parent.parent.parent.absolute())
        self.resources_dir_path = self.root_dir_path + '/resources'
        self.measurement_set_path = self.resources_dir_path + '/test.ms' # todo - to be set from config file

    def get_root_dir_path(self):
        return self.root_dir_path

    def get_resources_dir_path(self):
        return self.resources_dir_path

    def get_measurement_set_path(self):
        return self.measurement_set_path
