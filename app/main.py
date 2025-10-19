import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Роуты/логика
from .handlers import router

# Загружаем .env (чтобы BOT_TOKEN и ссылки подтянулись)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

async def main():
    if not BOT_TOKEN:
        # Запуск без токена не имеет смысла — просто аккуратно завершаемся.
        print("BOT_TOKEN отсутствует. Укажи его в .env")
        return

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot is starting polling…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
