import sys
import functools
import random
import hashlib
import requests
from langdetect import DetectorFactory, detect_langs
from config import settings


DetectorFactory.seed = 0


@functools.lru_cache(1)
def get_common_languages():
    res = set(settings.COMMON_LANGUAGES or [])
    res.add(settings.MAIN_LANGUAGE)
    res -= settings.AWS_NOT_SUPPORTED_LANGUAGES
    return res


def detect_language(text):
    src_code = detect_offline(text) or detect_baidu(text)
    if src_code is None:
        src_code = "auto"
    tar_code = get_target_language(src_code)
    if settings.DEBUG_MODE:
        print("Translating %s -> %s" % (src_code, tar_code))
    return src_code, tar_code


def get_target_language(src_code):
    main_language = settings.MAIN_LANGUAGE
    if main_language == "zh-cn":
        main_language = "zh"
    main_language = main_language.lower()
    if src_code is None or src_code == "auto":
        return main_language
    if src_code == main_language:
        for code in ["en", "zh", "zh-tw"]:
            if code in get_common_languages() and src_code != code:
                return code
        for code in get_common_languages():
            if code != src_code:
                return code
    return main_language


def detect_offline(text):
    src_codes = [item.lang for item in detect_langs(text)]
    for src_code in src_codes:
        if src_code in get_common_languages():
            if src_code == "zh-cn":
                return "zh"
            return src_code
    if settings.DEBUG_MODE:
        print("fail to detect language type offline")


def detect_baidu(text):

    def _handle_baidu_error(res):
        if res["error_code"] != 0 and settings.DEBUG_MODE:
            options = {
                52001: "请求超时",
                52002: "系统错误",
                52003: "未授权用户",
                54000: "必填参数为空",
                54001: "签名错误",
                54003: "访问频率受限",
                54004: "账户余额不足",
                54009: "语种检测失败",
                58000: "客户端IP非法",
                58002: "服务当前已关闭"
            }
            err_msg = "%s. %s" % (options.get(
                res["error_code"],
                "Unknown baidu API error"),
                res["error_msg"])
            print(err_msg, file=sys.stderr)
            raise Exception(err_msg)
        return res

    def _baidu_code_to_iso639(code):
        # map to ISO 639-1
        # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        special_codes = {
            "jp": "ja",  # 日语
            "kor": "ko",  # 韩语
            "vie": "vi",  # 越南语
        }
        return special_codes.get(code, code)

    if not settings.ENABLE_BAIDU_DETECTION:
        return
    endpoint = "https://fanyi-api.baidu.com/api/trans/vip/language"
    salt = str(random.randint(32768, 65536))
    sign = hashlib.md5(
        (settings.BAIDU_APP_ID +
         text +
         salt +
         settings.BAIDU_API_KEY).encode('utf-8')).hexdigest()
    payload = {
        "q": text,
        "appid": settings.BAIDU_APP_ID,
        "salt": salt,
        "sign": sign
    }
    try:
        res = requests.get(endpoint, params=payload).json()
        _handle_baidu_error(res)
        code = _baidu_code_to_iso639(res["data"]["src"])
        if code in get_common_languages():
            return code
    except Exception:
        if settings.DEBUG_MODE:
            raise
        return
    if settings.DEBUG_MODE:
        print("fail to detect language type by Baidu")
