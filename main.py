import argparse

from lib.app import create_app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--host", default="::", help="server host")
    parser.add_argument("-p", "--port", type=int, default=80, help="server port")
    parser.add_argument("-d", "--debug", action="store_true", help="flask debug")
    params, _ = parser.parse_known_args()

    app = create_app("sync-recording")
    app.run(host=params.host, port=params.port, debug=params.debug)


if __name__ == "__main__":
    main()
