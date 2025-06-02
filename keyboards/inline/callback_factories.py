from aiogram.filters.callback_data import CallbackData


class SettingsCallbackFactory(CallbackData, prefix="settings"):
    item: str


class LanguageCallbackFactory(CallbackData, prefix="language"):
    item: str


class ExchangesCallbackFactory(CallbackData, prefix="set_exchange"):
    exchange: str
    is_true: bool


class SetSpreadCallbackFactory(CallbackData, prefix="set_spread"):
    spread_type: str


class SetProfitCallbackFactory(CallbackData, prefix="set_profit"):
    profit_type: str


class SetVolumeCallbackFactory(CallbackData, prefix="set_volume"):
    volume_type: str
