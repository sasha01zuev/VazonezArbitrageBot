import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_language_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from utils.texts import TEXTS

router = Router()


@router.message(Command("language"), StateFilter("*"))
async def change_language(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    current_lang = await db.get_user_language(user_id=message.from_user.id)
    await message.answer(text=texts.commands.settings.language,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_language_keyboard(texts=texts, current_lang=current_lang,
                                                            is_from_settings=False)
                         )


@router.callback_query(SettingsCallbackFactory.filter(F.item == "language"), StateFilter("*"))
async def change_language(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    current_lang = await db.get_user_language(user_id=callback.from_user.id)
    await callback.message.edit_text(texts.commands.settings.language,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_language_keyboard(texts=texts, current_lang=current_lang,
                                                                        is_from_settings=True)
                                     )


@router.callback_query(LanguageCallbackFactory.filter(F.item), StateFilter("*"))
async def selected_language(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                            callback_data: LanguageCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    language = callback_data.item
    if language == 'ru':
        texts = TextProxy(data=TEXTS, lang='ru')
    elif language == 'en':
        texts = TextProxy(data=TEXTS, lang='en')

    user_current_lang = await db.get_user_language(user_id=callback.from_user.id)

    if language != user_current_lang:  # Не выбран ли текущий язык (Предотвращает ошибку message is not modified)
        await db.set_user_language(user_id=callback.from_user.id, language=language)
        await callback.answer(cache_time=1, text=texts.callback.language.language_changed)
        await callback.message.edit_text(texts.commands.settings.language,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_language_keyboard(texts=texts, current_lang=language,
                                                                            is_from_settings=True)
                                         )
    else:
        await callback.answer(cache_time=1)