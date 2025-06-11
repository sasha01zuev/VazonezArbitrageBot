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


class SetNetworkSpeedCallbackFactory(CallbackData, prefix="set_network_speed"):
    network_speed: int
    is_show_undefined_networks_chosen: bool
    show_undefined_networks: bool


class SetContractsCallbackFactory(CallbackData, prefix="set_profit"):
    contracts_type: bool


class SetWithdrawFeeCallbackFactory(CallbackData, prefix="set_withdraw_fee"):
    withdraw_fee_type: str


class SetCoinVolume24hCallbackFactory(CallbackData, prefix="set_spread"):
    coin_volume_24h_type: str


class SetLastTradeTimeCallbackFactory(CallbackData, prefix="set_last_trade_time"):
    last_trade_time_type: str


class SetNotificationCallbackFactory(CallbackData, prefix="set_notification"):
    notification: bool


class SetIsLowBidsCallbackFactory(CallbackData, prefix="set_is_low_bids"):
    is_low_bids: bool


class SetHedgingTypesCallbackFactory(CallbackData, prefix="set_hedging_types"):
    hedging_type: str


class SetFuturesHedgingCallbackFactory(CallbackData, prefix="set_futures_hedging"):
    hedging_value: bool


class SetMarginHedgingCallbackFactory(CallbackData, prefix="set_margin_hedging"):
    hedging_value: bool


class SetLoanHedgingCallbackFactory(CallbackData, prefix="set_loan_hedging"):
    hedging_value: bool


class SetBlacklistTypesCallbackFactory(CallbackData, prefix="set_blacklist_types"):
    blacklist_type: str

# region COINS BLACKLIST CALLBACK FACTORIES
class SetCoinsBlacklistCallbackFactory(CallbackData, prefix="set_coins_blacklist"):
    action: str


class SetCoinsBlacklistCoinCallbackFactory(CallbackData, prefix="set_coins_blacklist_coin"):
    coin: str


class SetCoinsInCoinsBlacklistCallbackFactory(CallbackData, prefix="set_coins_blacklist_coin"):
    coin: str
#endregion

# region NETWORKS BLACKLIST CALLBACK FACTORIES
class SetNetworksBlacklistCallbackFactory(CallbackData, prefix="set_networks_blacklist"):
    action: str


class SetNetworksBlacklistNetworkCallbackFactory(CallbackData, prefix="set_network_blacklist_network"):
    network: str


class SetNetworksInNetworksBlacklistCallbackFactory(CallbackData, prefix="set_networks_blacklist_coin"):
    network: str
#endregion


# region COIN FOR EXCHANGE BLACKLIST CALLBACK FACTORIES
class SetCoinForExchangeBlacklistCallbackFactory(CallbackData, prefix="set_coin_for_exchange_blacklist"):
    action: str


class SetCoinForExchangeBlacklistCoinForExchangeCoinCallbackFactory(CallbackData, prefix="set_cfe_blacklist_cfe"):
    coin_for_exchange: str
    action: str


class SelectExchangeForCoinForExchangeBlacklistCallbackFactory(CallbackData, prefix="sel_exc_for_bl_cfe"):
    exchange: str
    coin: str
    action: str
# endregion


class ArbitrageMenuCallbackFactory(CallbackData, prefix="arbitrage"):
    arbitrage_type: str
