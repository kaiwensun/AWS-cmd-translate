import sys
import requests
from config import settings


class Youdao:

    _err_codes = {
        0: u"正常 / ok",
        20: u"要翻译的文本过长 / text too long",
        30: u"无法进行有效的翻译 / failed to translate",
        40: "不支持的语言类型 / unsupported language type",
        50: u"无效的key / invalid API key",
        60: u"无词典结果，仅在获取词典结果生效 / No result"
    }

    def __init__(self):
        self._base_payload = {
            "keyfrom": settings.YOUDAO_APP_NAME,
            "key": settings.YOUDAO_API_KEY,
            "type": "data",
            "doctype": "json",
            "version": "1.1"
        }

    def lookup(self, source_text):
        payload = {
            **self._base_payload,
            "q": source_text
        }
        self.last_source_text = source_text
        base_url = "http://fanyi.youdao.com/openapi.do"
        try:
            res = requests.get(base_url, params=payload)
            if res.status_code == 403:
                # Youdao is blocked by internet service provider
                if settings.DEBUG_MODE:
                    print("Youdao is blocked", file=sys.stderr)
                return
            elif settings.DEBUG_MODE and res.status_code != 200:
                print(res.text, file=sys.stderr)
                print(res.text, file=sys.reason)
        except Exception:
            print("请检查网络连接")
            if settings.DEBUG_MODE:
                raise
            return
        if getattr(res, "text", None) == 'no query':
            print("无效的输入")
            return
        return res.json()

    def display(self, result):
        found = False
        err_code = result["errorCode"]
        if err_code:
            print(self._err_codes[err_code])
            return
        if settings.YOUDAO_DISPLAY_PHONETIC:
            phonetic_types = ["phonetic", "uk-phonetic", "us-phonetic"]
            for phonetic_type in phonetic_types:
                if result.get("basic", {}).get(phonetic_type):
                    print("[%s]" % result["basic"][phonetic_type])
                    break

        dedup = set()
        if settings.YOUDAO_DISPLAY_BASIC:
            for basic_explain in result.get("basic", {}).get("explains", []):
                if basic_explain not in dedup:
                    dedup.add(basic_explain)
                    print(basic_explain)
                    found = True

        if settings.YOUDAO_DISPLAY_TRANSLATION:
            for translation in result.get("translation", []):
                if translation != self.last_source_text \
                        and translation not in dedup:
                    dedup.add(translation)
                    print(translation)
                    found = True
        if settings.YOUDAO_DISPLAY_WEB:
            for web_result in result.get("web", []):
                if web_result.get("key") and web_result.get("value"):
                    print()
                    print(web_result["key"])
                    for value in web_result["value"]:
                        print(" - %s" % value)
                    found = True
        if not found:
            print("没有找到翻译")
