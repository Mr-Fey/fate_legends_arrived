import json
from settings import cwd
from functools import lru_cache
from typing import Any

LOCALES_DIR = cwd / "json" / "locales"
FALLBACK_LOCALE = "en-US"


@lru_cache(maxsize=None)
def _load_locale(locale: str) -> dict[str, str]:
    file_path = LOCALES_DIR / f"{locale}.json"
    if not file_path.exists():
        return _load_locale(FALLBACK_LOCALE)

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {str(key): str(value) for key, value in data.items()}


def _normalize_locale(locale: Any) -> str:
    if locale is None:
        return FALLBACK_LOCALE

    value = getattr(locale, "value", locale)
    value = str(value).strip()
    if not value:
        return FALLBACK_LOCALE

    normalized = value.replace("_", "-")
    mapping = {
        "en": FALLBACK_LOCALE,
        "en-US": FALLBACK_LOCALE,
        "en-us": FALLBACK_LOCALE,
        "ru": "ru",
        "ru-RU": "ru",
        "uk": "uk",
        "uk-UA": "uk",
    }
    return mapping.get(normalized, mapping.get(normalized.lower(), FALLBACK_LOCALE))


def translate(key: str, locale: Any = None, **values: Any) -> str:
    resolved_locale = _normalize_locale(locale)
    translations = _load_locale(resolved_locale)
    fallback = _load_locale(FALLBACK_LOCALE)
    template = translations.get(key, fallback.get(key, key))

    if not values:
        return template
    try:
        return template.format(**values)
    except (KeyError, IndexError, ValueError):
        return template
