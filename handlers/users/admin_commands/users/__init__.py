from .add_user_to_blacklist import admin_users_router


routers_list = [
    admin_users_router
]


__all__ = [
    "routers_list",
]