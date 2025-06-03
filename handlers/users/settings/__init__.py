from .language import router as language_router
from .exchanges import router as exchanges_router
from .spread import router as spread_router
from .profit import router as profit_router
from .volume import router as volume_router
from .network_speed import router as network_speed_router
from .contracts import router as contracts_router
from .withdraw_fee import router as withdraw_fee_router
from .coin_volume_24h import router as coin_volume_24h_router

routers = [language_router, exchanges_router, spread_router, profit_router, volume_router, network_speed_router,
           contracts_router, withdraw_fee_router, coin_volume_24h_router]