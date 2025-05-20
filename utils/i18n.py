from utils.texts import TEXTS


class TextProxy:
    def __init__(self, data: dict, lang: str, fallback: str = "ru"):
        self._data = data
        self._lang = lang
        self._fallback = fallback

    def __getattr__(self, item):
        value = self._data.get(item)

        if isinstance(value, dict):
            # Если это словарь с языками, и там есть нужный язык — вернуть строку
            if self._lang in value or self._fallback in value:
                return value.get(self._lang) or value.get(self._fallback)
            return TextProxy(value, self._lang, self._fallback)

        return value
