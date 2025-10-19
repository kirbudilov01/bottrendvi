import asyncio, os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from .handlers import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    # Не паникуем в GitHub, но для запуска понадобится токен
    print("WARNING: BOT_TOKEN is empty. Fill it in .env on the server or local env.")

async def main():
    if not BOT_TOKEN:
        # Чтобы файл импортировался без аварий — не запускаем polling без токена.
        print("Bot is not started because BOT_TOKEN is missing.")
        return
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
