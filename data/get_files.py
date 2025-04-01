import json
from pathlib import Path
import aiofiles


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CHANNEL_DIR = BASE_DIR / "data/channel"
DATA_USERS_DIR = BASE_DIR / "data/users"

is_channel_monitoring_available_path = DATA_CHANNEL_DIR / "is_monitoring_available.json"


# Асинхронная функция для загрузки is_channel_monitoring_available из JSON-файла
async def load_channel_monitoring_available(filepath: str = is_channel_monitoring_available_path):
    async with aiofiles.open(filepath, "r") as file:
        content = await file.read()
        return json.loads(content)
