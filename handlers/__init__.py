from .users import routers_list as users_router
# from .channels import routers_list as channels_router


routers_list = [
    *users_router  # * - распаковка списка
]

__all__ = [
    "routers_list",
]
