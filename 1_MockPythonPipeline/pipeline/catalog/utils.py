from pathlib import Path
from pipeline.base_logger import logger
from pipeline.catalog.catalog import Source
from astropy.coordinates import SkyCoord


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

    def read_catalog_file(self, filename):
        file_path = self.resources_dir_path + f'/{filename}'
        sources = []
        with open(file_path) as file:
            for line in file:
                if line.startswith("#"):
                    continue
                ra, dec, brightness = line.replace(" ", "").rstrip("\n").split(',')
                sources.append(Source(SkyCoord(ra, dec, frame="fk5"), brightness))
                logger.debug(f"source with "
                             f"coordinates ({ra},{dec}) and brightness {brightness} "
                             f"read from catalog file: {filename}")

        logger.info(f"{len(sources)} read from catalog file: {filename}")
        return sources
