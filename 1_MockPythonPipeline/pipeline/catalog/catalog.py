from typing import List
from astropy.coordinates import SkyCoord
from pipeline.base_logger import logger
from pipeline.catalog.utils import Utilities

utils = Utilities()


class Source:
    def __init__(self, coordinates, brightness):
        self.coordinates = coordinates
        self.brightness = brightness
        logger.debug(f"new source constructed with "
                     f"coordinates: ({coordinates.to_string(style='hmsdms')}) "
                     f"and brightness {brightness} units")

    def get_coordinates(self):
        return self.coordinates

    def get_brightness(self):
        return self.brightness

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_brightness(self, brightness):
        self.brightness = brightness

    def get_info(self):
        return f"source has " \
               f"coordinates: ({self.coordinates.to_string(style='hmsdms')}) " \
               f"and brightness {self.brightness} units"


class Catalog:
    def __init__(self, name):
        self.name = name
        self.sources: List[Source] = []
        logger.debug(f"new catalog constructed with name: ({name})")

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def add_sources(self, sources):
        self.sources.extend(sources)
        logger.debug(f"{len(sources)} new sources added to catalog ({self.name})")

    def get_info(self):
        return f"catalog ({self.name}) " \
               f"has {len(self.sources)} sources"

    def read_catalog_file(self, filename):
        file_path = utils.get_resources_dir_path() + f'/{filename}'
        sources = []
        with open(file_path) as file:
            for line in file:
                if line.startswith("#"):
                    continue
                ra, dec, brightness = line.replace(" ", "").rstrip("\n").split(',')
                sources.append(Source(SkyCoord(ra, dec, frame="fk5"), brightness))
                logger.debug(f"source with "
                             f"coordinates ({ra},{dec}) and brightness {brightness} "
                             f"read from catalog file: {filename} "
                             f"for catalog {self.name}")

        logger.info(f"{len(sources)} read from catalog file: {filename} "
                    f"for catalog {self.name}")
        return sources

    def read_catalog_files(self, filename_list):
        sources = []
        for filename in filename_list:
            sources.extend(self.read_catalog_file(filename))
        logger.info(f"catalog files {filename_list} read into catalog {self.name}")
        self.add_sources(sources)

