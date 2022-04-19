from astropy.coordinates import SkyCoord

from pipeline.base_logger import logger
from pipeline.catalog.catalog import Catalog, Source
from pipeline.catalog.utils import Utilities


def do_something():
    logger.info("this is info logging in run")
    logger.debug("this is debug logging in run")

    utils = Utilities()


    sources = utils.read_catalog_file("1.cat")
    logger.info(sources[0].get_info())
    logger.info(sources[1].get_info())
    logger.info(len(sources))



if __name__ == '__main__':
    logger.getLogger().setLevel(logger.DEBUG)
    do_something()