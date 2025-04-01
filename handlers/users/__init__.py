from .admin_commands import routers_list as admin_commands_router
from .start import start_router
from .echo import echo_router

routers_list = [
    *admin_commands_router,
    start_router,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
