from .common_statistics import router as common_statistics_router
from .withdraw import router as withdraw_router
from .convert_to_subscription import router as convert_to_subscription_router

routers = [common_statistics_router, withdraw_router, convert_to_subscription_router]
