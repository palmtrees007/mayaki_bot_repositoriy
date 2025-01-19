import asyncio

import os

from aiogram import Bot, Dispatcher

from config.config import load_config
from handlers.handlers import router


async def main():
    config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    photo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos')
    text_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'texts')
    link_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'links')
    dp.include_router(router)
    dp.workflow_data.update({'pages': 3, 'all_media_dir': photo_dir, 'text_dir': text_dir, 'link_dir': link_dir})
    await dp.start_polling(bot)

asyncio.run(main())