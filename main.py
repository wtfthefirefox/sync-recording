import argparse

from lib.app import create_app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--host", default="0.0.0.0", help="server host")
    parser.add_argument("-p", "--port", type=int, default=8081, help="server port")
    parser.add_argument("-d", "--debug", action="store_true", help="flask debug")
    parser.add_argument("--config-path", default="./settings.yaml", help="recorder yaml config path")
    params = parser.parse_args()

    app = create_app("sync-recording", params.config_path)
    app.run(host=params.host, port=params.port, debug=params.debug)


if __name__ == "__main__":
    main()
