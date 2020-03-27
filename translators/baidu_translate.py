import sys
import requests
import random
import hashlib
import requests
from config import settings
import functools


class BaiduTranslate:

    def lookup(self, source_text, src_code, tar_code):

        def _handle_baidu_error(res):
            if res.get("error_code", 0) != 0 and settings.DEBUG_MODE:
                options = {
                    52001: "请求超时",
                    52002: "系统错误",
                    52003: "未授权用户",
                    54000: "必填参数为空",
                    54001: "签名错误",
                    54003: "访问频率受限",
                    54004: "账户余额不足",
                    54005: "长query请求频繁",
                    58000: "客户端IP非法",
                    58001: "译文语言方向不支持",
                    58002: "服务当前已关闭",
                    90107: "认证未通过或未生效"
                }
                err_msg = "%s. %s" % (options.get(
                    res["error_code"],
                    "Unknown baidu API error"),
                    res["error_msg"])
                print(err_msg, file=sys.stderr)
                raise Exception(err_msg)
            return res

        src_code = self._iso639_to_baidu(src_code)
        tar_code = self._iso639_to_baidu(tar_code)
        endpoint = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        salt = str(random.randint(0x8000, 0x7FFFFFFF))
        sign = hashlib.md5(
            (settings.BAIDU_APP_ID +
             source_text +
             salt +
             settings.BAIDU_API_KEY).encode('utf-8')).hexdigest()
        payload = {
            "q": source_text,
            "from": src_code,
            "to": tar_code,
            "appid": settings.BAIDU_APP_ID,
            "salt": salt,
            "sign": sign
        }
        try:
            res = requests.get(endpoint, params=payload).json()
            return _handle_baidu_error(res)
        except Exception:
            if settings.DEBUG_MODE:
                raise
            return

    def display(self, result):
        if result["trans_result"]:
            print(result["trans_result"][0]["dst"])

    @functools.lru_cache(None)
    def _iso639_to_baidu(self, code):
        if code is None or code == "auto":
            return code
        if code == "zh-tw":
            return "cht"
        code = code[:2]
        special_codes = {
            "ja": "jp",
            "ko": "kor",
            "fr": "fra",
            "es": "spa",
            "ar": "ara",
            "pg": "bul",
            "et": "est",
            "da": "dan",
            "fi": "fin",
            "ro": "rom",
            "sk": "slo",
            "sv": "swe",
            "vi": "vie"
        }
        return special_codes.get(code, code)
