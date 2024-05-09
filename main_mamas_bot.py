#!/usr/bin/env python3
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher  # , Router, types
from aiogram.enums import ParseMode
from routing import router
from conf import token

bot = Bot(token=token, parse_mode=ParseMode.HTML)


async def main() -> None:

    dp = Dispatcher()
    dp.include_routers(router)  #  must be at the end

    tasks = [dp.start_polling(bot)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt: ", e)
