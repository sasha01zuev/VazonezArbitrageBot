from utils.texts import TEXTS


class TextProxy:
    def __init__(self, data: dict, lang: str, fallback: str = "ru"):
        self._data = data
        self._lang = lang
        self._fallback = fallback

        self._known_langs = {"ru", "en", "ua", "uk", "es", "de", "fr"}

    def __getattr__(self, item):
        value = self._data.get(item)

        if value is None:
            raise AttributeError(f"TextProxy: ключ '{item}' не найден.")

        # 🔥 Если значение — словарь, и его ключи это только языки
        if isinstance(value, dict):
            keys = set(value.keys())

            if keys.issubset(self._known_langs):
                # ✅ Это финальный слой: возвращаем локализованную строку
                return value.get(self._lang) or value.get(self._fallback)

            # Иначе продолжаем оборачивать
            return TextProxy(value, self._lang, self._fallback)

        # Если это уже строка или что-то ещё — возвращаем как есть
        return value

    def __str__(self):
        # Даже если внутри есть неязыковые ключи — всё равно финализируем, если языковой ключ есть
        if isinstance(self._data, dict):
            if self._lang in self._data or self._fallback in self._data:
                value = self._data.get(self._lang) or self._data.get(self._fallback)
                if isinstance(value, str):
                    return value

        if isinstance(self._data, str):
            return self._data

        raise TypeError("TextProxy не может быть приведён к строке (не найден текст по языку)")

