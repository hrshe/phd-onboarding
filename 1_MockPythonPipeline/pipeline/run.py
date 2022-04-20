from pipeline.base_logger import logger
from pipeline.catalog.catalog import Catalog
import argparse

from pipeline.catalog.utils import Utilities

arg_parser = argparse.ArgumentParser(description="a mock pipeline to simulate sources")
utils = Utilities()

def do_something():
    utils.set_measurement_set_path('test.ms')

    logger.info("this is info logging in run")
    logger.debug("this is debug logging in run")

    cat1 = Catalog("test catalog")
    cat1.read_catalog_files(["1.cat", "2.cat"])
    logger.info(cat1.get_info())


if __name__ == '__main__':
    arg_parser.add_argument('-m', '--msrset', type=str, )
    logger.getLogger().setLevel(logger.DEBUG)
    do_something()
