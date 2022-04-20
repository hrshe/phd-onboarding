from pipeline.argument_parser import arg_parser
from pipeline.base_logger import logger
from pipeline.catalog.catalog import Catalog

from pipeline.catalog.utils import Utilities

utils = Utilities()


def do_something(ms_filename, cat_filename_list):
    utils.set_measurement_set_path(ms_filename)

    cat1 = Catalog("test catalog")
    cat1.read_catalog_files(cat_filename_list)
    logger.info(cat1.get_info())


if __name__ == '__main__':
    arguments = arg_parser.parse_args()
    if arguments.verbose:
        logger.getLogger().setLevel(logger.DEBUG)
        logger.info("printing logs in verbose")
    do_something(arguments.msr_set, arguments.cat_list)
