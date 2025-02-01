import sys

from loguru import logger

from app import create_app
from configs.prod_config import ProdConfig

application = create_app(ProdConfig)
logger.debug(f"Created {application = }")


def main(host: str = "0.0.0.0", port: int = 5000):
    logger.debug(f"{host = } {port = }")
    application.run(host=host, port=port, debug=True)  # run using development server.


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a]
    if len(args) == 2:
        logger.info("Using supplied host and port arguments ... ")
        main(*args)
    else:
        main()
