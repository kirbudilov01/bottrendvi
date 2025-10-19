# Telegram Viral Shorts Bot (no DB)

## Что сделано
- RU/EN/ZH → согласие → главное меню.
- Виральные shorts: «Добавить ключ» — отправляем ключ на DEV_WEBHOOK_URL (ключи не храним).
- Полезные фишки: приглашение, TON, поддержка.

## Переменные окружения
Скопируй `.env.example` → `.env` и заполни значения:
- `BOT_TOKEN` — токен телеграм-бота
- `DEV_WEBHOOK_URL` — ваш endpoint для приёма ключа
- `ABOUT_URL`, `LOGIN_URL`, `SUPPORT_URL`, `TON_ADDRESS`

## Структура
