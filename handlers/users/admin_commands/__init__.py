from .channel import routers_list as admin_channel_router
from .users import routers_list as admin_users_router

routers_list = [
    *admin_channel_router,
    *admin_users_router
]

__all__ = [
    "routers_list",
]
