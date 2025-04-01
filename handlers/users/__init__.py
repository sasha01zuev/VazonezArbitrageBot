from .start import start_router
from .echo import echo_router

routers_list = [
    start_router,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]