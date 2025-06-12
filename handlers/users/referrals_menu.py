from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
import logging

from aiogram.utils.deep_linking import create_start_link

from keyboards.inline import get_main_keyboard, get_referral_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy

referral_router = Router()


@referral_router.message(Command("referral_program"), StateFilter("*"))
async def referrals_handler(message: Message, db: Database, texts: TextProxy, state: FSMContext, bot: Bot):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_referral_link = await create_start_link(bot=bot, payload=f"ref-{message.from_user.id}",)
    await message.answer(text=texts.commands.referrals.set_referrals.format(user_referral_link=user_referral_link),
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_referral_keyboard(texts=texts, user_referral_link=user_referral_link))


@referral_router.callback_query(F.data == "referrals", StateFilter("*"))
async def referrals_handler(call: Message, db: Database, texts: TextProxy, state: FSMContext, bot: Bot):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")

    await state.clear()

    await call.answer(cache_time=1)
    user_referral_link = await create_start_link(bot=bot, payload=f"ref-{call.from_user.id}",)
    await call.message.edit_text(
        text=texts.commands.referrals.set_referrals.format(user_referral_link=user_referral_link),
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_referral_keyboard(texts=texts, user_referral_link=user_referral_link))
