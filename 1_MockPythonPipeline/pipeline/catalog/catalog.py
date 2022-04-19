from typing import List
from pipeline.base_logger import logger


class Catalog:
    def __init__(self, name):
        self.name = name
        self.sources: List[Source] = []
        logger.debug(f"catalog constructed with name: ({name})")

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


class Source:
    def __init__(self, coordinates, brightness):
        self.coordinates = coordinates
        self.brightness = brightness
        logger.debug(f"source constructed with "
                     f"coordinates: ({coordinates.to_string(style='hmsdms')}) "
                     f"and brightness {brightness}")

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
               f"and brightness {self.brightness}"
