import argparse
from typing import List
from typing import NoReturn

import yaml

from pictureresponsebot.PictureResponseBot import PictureResponseBot


def main(args: List[str] = None) -> NoReturn:
    parser = argparse.ArgumentParser(description="Run a Telegram bot that can respond with a specified picture")
    parser.add_argument('-c', '--config', type=str, help='set path of config file', required=True)
    args = parser.parse_args()
    config = args.config
    try:
        with open(config) as f:
            config_data = yaml.safe_load(f)
    except (FileNotFoundError, TypeError) as e:
        print(f"{e.strerror} -- could not find '{config}'")
    else:
        picture_response_bot: PictureResponseBot = PictureResponseBot(**config_data)


if __name__ == "__main__":
    main()
