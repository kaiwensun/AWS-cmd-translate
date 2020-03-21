import sys
_NOT_SET_ = "_NOT_SET_"

# These settings can be overridden by local_settings.py
DEBUG_MODE = False
MAIN_LANGUAGE = "zh"
AWS_NOT_SUPPORTED_LANGUAGES = ["ca", "cy", "gu", "kn", "lt", "mk", "ml", "mr", "ne", "pa", "te"]

# AWS Translate client
AWS_REGION_NAME = None
AWS_API_VERSION = None
AWS_ENDPOINT_URL = None
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_SESSION_TOKEN = None

# Overriding
thismodule = sys.modules[__name__]
try:
    from config import local_settings
    for key in dir(local_settings):
        setattr(thismodule, key, getattr(local_settings, key))
except ModuleNotFoundError:
    pass

for key in dir(thismodule):
    if key is not "_NOT_SET_" and getattr(thismodule, key) is _NOT_SET_:
        raise AttributeError("%s should be set in local_settings." % key)
