from aiogram import Router, F, Bot
from aiogram.types import Message

echo_router = Router()


@echo_router.message(F.photo)
async def answer_photo(message: Message, bot: Bot):
    """Answer for photo-message"""
    await message.answer("Я пока-что не принимаю фото! 🤨😲")
    await bot.send_photo(chat_id=609200395, photo=message.photo[-1].file_id)


@echo_router.message(flags={"throttling_rate_limit": 5})
async def answer_message(message: Message):
    """Answer for simple message"""
    await message.answer(f"<b>{message.text}</b>", parse_mode="HTML")
