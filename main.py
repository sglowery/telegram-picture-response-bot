from typing import List, NoReturn

from pictureresponsebot.PictureResponseBot import PictureResponseBot
from pictureresponsebot.config import TOKEN


def main(args: List[str] = None) -> NoReturn:
    picture_response_bot: PictureResponseBot = PictureResponseBot(token=TOKEN)
    picture_response_bot.run()


if __name__ == "__main__":
    main()
