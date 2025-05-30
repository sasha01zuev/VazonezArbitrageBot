from .language import router as language_router
from .exchanges import router as exchanges_router
from .spread import router as spread_router

routers = [language_router, exchanges_router, spread_router]