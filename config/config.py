from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
MAIN_ADMIN = int(env("MAIN_ADMIN"))
ADMINS_ID = env.list("ADMINS_ID")
