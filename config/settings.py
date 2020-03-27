import sys
import collections
import importlib
_NOT_SET_ = "_NOT_SET_"

# These settings can be overridden by local_settings.py

# Basic settings
DEBUG_MODE = False
COMMON_LANGUAGES = [
    'en', 'zh', 'zh-cn', 'zh-tw'
] # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

# Trnaslation Engines (class names)
ENGINES = [
    'amazon_translate'
]
ONLY_ONE_ENGINE = False
DISPLAY_SOURCE_DICT = False
ENABLE_BAIDU_DETECTION = False

# AWS Translate settings
# AWS Translate client
AWS_REGION_NAME = None
AWS_API_VERSION = None
AWS_ENDPOINT_URL = None
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_SESSION_TOKEN = None

# Basic AWS Translate settings
MAIN_LANGUAGE = "zh"
AWS_SUPPORTED_LANGUAGES = {"af", "sq", "am", "ar", "az", "bn", "bs", "bg", "zh", "zh-TW", "hr",
    "cs", "da", "fa-AF", "nl", "en", "et", "fi", "fr", "fr-CA", "ka", "de", "el", "ha", "he",
    "hi", "hu", "id", "it", "ja", "ko", "lv", "ms", "no", "fa", "ps", "pl", "pt", "ro", "ru",
    "sr", "sk", "sl", "so", "es", "sw", "sv", "tl", "ta", "th", "tr", "uk", "ur", "vi"}
AWS_NOT_SUPPORTED_LANGUAGES = {"ca", "cy", "gu", "kn", "lt", "mk", "ml", "mr", "ne", "pa", "te"}

# Youdao settings
YOUDAO_DISPLAY_BASIC = True
YOUDAO_DISPLAY_PHONETIC = True
YOUDAO_DISPLAY_TRANSLATION = True
YOUDAO_DISPLAY_WEB = True

# Do overriding
thismodule = sys.modules[__name__]
try:
    from config import local_settings
    for key in dir(local_settings):
        setattr(thismodule, key, getattr(local_settings, key))
except ImportError:
    pass

for key in dir(thismodule):
    if key is not "_NOT_SET_" and getattr(thismodule, key) is _NOT_SET_:
        raise AttributeError("%s should be set in local_settings." % key)
