import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from .handlers import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

async def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN отсутствует. Укажи его в .env")
        return

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot is starting polling…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
