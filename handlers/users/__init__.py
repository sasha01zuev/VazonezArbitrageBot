from .admin_commands import routers_list as admin_commands_router

from .settings import routers as settings_routers
from .menu import menu_router
from .referrals import referral_router
from .settings_menu import settings_menu_router
from .start import start_router
from .echo import echo_router

routers_list = [
    *admin_commands_router,
    start_router,
    menu_router,
    referral_router,
    settings_menu_router,

    *settings_routers,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
