from pipeline.base_logger import logger


def do_something():
    logger.info("this is info logging in run")
    logger.debug("this is debug logging in run")


if __name__ == '__main__':
    logger.getLogger().setLevel(logger.INFO)
    do_something()