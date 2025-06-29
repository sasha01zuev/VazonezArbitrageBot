from .language import router as language_router
from .exchanges import router as exchanges_router
from .spread import router as spread_router
from .profit import router as profit_router
from .volume import router as volume_router
from .network_speed import router as network_speed_router
from .contracts import router as contracts_router
from .withdraw_fee import router as withdraw_fee_router
from .coin_volume_24h import router as coin_volume_24h_router
from .last_trade_time import router as last_trade_time_router
from .notification import router as notification_router
from .is_low_bids import router as is_low_bids_router
from .hedging import router as hedging_types_router
from .blacklist import router as blacklist_types_router
from .blacklist_coins import router as blacklist_coins_router
from .blacklist_networks import router as blacklist_networks_router
from .blacklist_coin_for_exchange import router as blacklist_coins_for_exchange_router

routers = [language_router, exchanges_router, spread_router, profit_router, volume_router, network_speed_router,
           contracts_router, withdraw_fee_router, coin_volume_24h_router, last_trade_time_router, notification_router,
           is_low_bids_router, hedging_types_router, blacklist_types_router, blacklist_coins_router,
           blacklist_networks_router, blacklist_coins_for_exchange_router]