from pipeline.base_logger import logger
from pipeline.catalog.catalog import Catalog


def do_something():
    logger.info("this is info logging in run")
    logger.debug("this is debug logging in run")

    cat1 = Catalog("test catalog")
    cat1.read_catalog_files(["1.cat", "2.cat"])
    logger.info(cat1.get_info())


if __name__ == '__main__':
    logger.getLogger().setLevel(logger.DEBUG)
    do_something()
