from app import create_app
from configs.prod_config import ProdConfig

application = create_app(ProdConfig)


def main(host: str = "0.0.0.0", port: int = 5000):
    application.run(host=host, port=port, debug=True)  # run using development server.


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
