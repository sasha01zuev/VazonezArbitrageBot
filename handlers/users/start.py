from trace import Trace

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
import logging

from sqlalchemy.testing.suite.test_reflection import users

from keyboards.inline import get_main_keyboard, get_language_keyboard, LanguageCallbackFactory, \
    get_referrer_invite_notification_keyboard
from services.database.postgresql import Database
from states import SetLanguageStartGroup
from utils.i18n import TextProxy
from utils.texts import TEXTS
from config.config import MAIN_ADMIN

start_router = Router()


@start_router.message(CommandStart(deep_link=True, magic=F.args.regexp(r'ref-(\d+)').group(1).cast(int).as_('ref_id')),
                      StateFilter("*"))
async def change_language_start_handler_deeplink(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                                 db: Database, ref_id: int):
    if await state.get_state() is not None:
        if await state.get_state() in [SetLanguageStartGroup.SetLanguage]:
            pass
        else:
            logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
            await message.answer(text=texts.commands.state.canceled_state,
                                 disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    user_id = message.from_user.id

    # region ПРОВЕРКА РЕФЕРАЛЬНОГО USER ID
    is_referrer_valid = await db.get_user(user_id=ref_id)

    if user_id != ref_id:
        if is_referrer_valid:
            already_referred = await db.check_if_user_already_referred(user_id)

            if not already_referred:
                is_user_recently_registered = await db.is_user_recently_registered(user_id)

                if is_user_recently_registered:
                    await db.add_referral(user_id=ref_id, referral_id=user_id)

                    # region ИНФОРМИРУЕМ РЕФЕРЕРА О ПРИГЛАШЕНИИ
                    await db.add_referrals_quantity(user_id=ref_id)
                    await bot.send_message(ref_id, text=texts.commands.start.referral_invitation.format(
                        first_name=message.from_user.first_name), disable_notification=True, parse_mode="HTML",
                                             reply_markup=get_referrer_invite_notification_keyboard(texts=texts)
                    )
                    await bot.send_message(MAIN_ADMIN, f'<code>{ref_id}</code> пригласил <code>{user_id}</code> '
                                           f'@{message.from_user.username}', disable_notification=True,
                                           parse_mode="HTML")
                    # endregion

    # endregion

    current_lang = await db.get_user_language(user_id=user_id)
    await message.answer(text=texts.commands.settings.language,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_language_keyboard(texts=texts, current_lang=current_lang,
                                                            is_from_settings=False, is_start_command=True)
                         )
    await state.set_state(SetLanguageStartGroup.SetLanguage)
    await state.update_data(ref=ref_id)


@start_router.message(CommandStart(), StateFilter("*"))
async def change_language_start_handler(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        if await state.get_state() in [SetLanguageStartGroup.SetLanguage]:
            pass
        else:
            logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
            await message.answer(text=texts.commands.state.canceled_state,
                                 disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    current_lang = await db.get_user_language(user_id=message.from_user.id)
    await message.answer(text=texts.commands.settings.language,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_language_keyboard(texts=texts, current_lang=current_lang,
                                                            is_from_settings=False, is_start_command=True)
                         )
    await state.set_state(SetLanguageStartGroup.SetLanguage)
    await state.update_data(ref=None)


@start_router.callback_query(LanguageCallbackFactory.filter(F.item), SetLanguageStartGroup.SetLanguage)
async def start_handler_callback(callback: CallbackQuery, db: Database, texts: TextProxy, state: FSMContext,
                                 callback_data: LanguageCallbackFactory):
    language = callback_data.item
    await db.set_user_language(user_id=callback.from_user.id, language=language)

    state_data = await state.get_data()
    referral = state_data.get('ref')
    await state.clear()
    logging.debug(f"Реферальный код из состояния: {referral}")

    user_id = callback.from_user.id

    if language == 'ru':
        texts = TextProxy(data=TEXTS, lang='ru')
    elif language == 'en':
        texts = TextProxy(data=TEXTS, lang='en')

    if referral:
        logging.debug(f"Реферальное приглашение: {referral} для пользователя {user_id}")

    await callback.message.edit_text(text=texts.commands.start.welcome,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_main_keyboard(texts=texts))
