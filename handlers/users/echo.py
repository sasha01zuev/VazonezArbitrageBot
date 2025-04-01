from aiogram import Router, F, Bot
from aiogram.types import Message
from utils.misc.throttling import rate_limit

echo_router = Router()


@rate_limit()  # Anti-spam
@echo_router.message(F.photo)
async def answer_photo(message: Message, bot: Bot):
    """Answer for photo-message"""
    await message.answer("Я пока-что не принимаю фото! 🤨😲")
    await bot.send_photo(chat_id=609200395, photo=message.photo[-1].file_id)


@rate_limit()  # Anti-spam
@echo_router.message()
async def answer_message(message: Message):
    """Answer for simple message"""
    await message.answer(f"<b>{message.text}</b>", parse_mode="HTML")
