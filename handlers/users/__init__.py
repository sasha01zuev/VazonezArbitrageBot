from .admin_commands import routers_list as admin_commands_router

from .settings import routers as settings_routers

from .arbitrage_menu import arbitrage_menu_router
from .menu import menu_router
from .referrals_menu import referral_router
from .referrals import routers as referrals_statistics_routers
from .subscriptions_menu import subscriptions_menu_router
from .subscriptions import routers as subscriptions_routers
from .arbitrage import routers as arbitrage_routers

from .settings_menu import settings_menu_router
from .start import start_router
from .echo import echo_router

routers_list = [
    *admin_commands_router,
    start_router,
    menu_router,
    referral_router,
    subscriptions_menu_router,
    arbitrage_menu_router,
    settings_menu_router,

    *subscriptions_routers,
    *referrals_statistics_routers,
    *arbitrage_routers,
    *settings_routers,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
