import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiohttp import web
from .handlers import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
PORT = int(os.getenv("PORT", "8923"))

async def create_app(bot: Bot):
    app = web.Application()

    async def send_message(request: web.Request):
        try:
            data = await request.json()
            chat_id = data["chat_id"]
            text = data["text"]
        except Exception:
            return web.json_response(
                {"ok": False, "error": "Invalid JSON or missing fields"},
                status=400,
            )

        try:
            await bot.send_message(chat_id=chat_id, text=text)
            return web.json_response({"ok": True})
        except Exception as e:
            return web.json_response(
                {"ok": False, "error": str(e)},
                status=500,
            )

    app.router.add_post("/send", send_message)
    return app

async def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN отсутствует. Укажи его в .env")
        return

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(router)

    app = await create_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()

    sockets = site._server.sockets
    if sockets:
        actual_port = sockets[0].getsockname()[1]
        print(f"HTTP server started on port {actual_port}")

    print("Bot is starting polling…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
