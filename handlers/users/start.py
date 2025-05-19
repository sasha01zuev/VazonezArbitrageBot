from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from services.database.postgresql import Database

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, db: Database):
    user = await db.get_user(user_id=message.from_user.id)

    if not user:
        user_language = message.from_user.language_code

        await db.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            language='ru'
        )

        await message.answer("Ты не был зарегистрирован, но теперь ты зарегистрирован!")
    else:
        await message.answer(
            "🚀 <b>Arbitrage Screener</b>\n\n"
            "- Больше 20 криптобирж\n"
            "- Обновление каждые 5 секунд\n"
            "- Максимальная фильтрация связок\n\n"
            "🎁 Приглашай пользователей и получай вознаграждения.",
            disable_web_page_preview=True, parse_mode="HTML")


@start_router.message(F.from_user.id.in_([609200395, 2342332534]), F.text == "123")
async def start_handler(message: Message, db: Database):
    # user = await db.get_user(user_id=message.from_user.id)
    await message.answer("456")