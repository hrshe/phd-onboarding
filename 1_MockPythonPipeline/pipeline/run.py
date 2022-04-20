from pipeline.base_logger import logger
from pipeline.catalog.catalog import Catalog
import argparse

from pipeline.catalog.utils import Utilities

arg_parser = argparse.ArgumentParser(description="a mock pipeline to simulate sources")
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action='store_true', help='print quietly(default)')
group.add_argument('-v', '--verbose', action='store_true', help='print verbose')
utils = Utilities()

def do_something():
    utils.set_measurement_set_path('test.ms')

    cat1 = Catalog("test catalog")
    cat1.read_catalog_files(["1.cat", "2.cat"])
    logger.info(cat1.get_info())


if __name__ == '__main__':
    arg_parser.add_argument('-s', '--msr_set', type=str, metavar="", required=True,
                            help="measurement set filename (in resources folder)")

    arg_parser.add_argument('-l', '--list', nargs='+', metavar="", required=True,
                            help='cat filename list (in resources folder)')

    arguments = arg_parser.parse_args()
    if arguments.verbose:
        logger.getLogger().setLevel(logger.DEBUG)
        logger.info("printing logs in verbose")
    do_something()
