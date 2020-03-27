import sys
import requests
import random
import hashlib
import requests
from config import settings
import functools


class ICiba:

    def lookup(self, source_text, src_code, tar_code):
        for code in [src_code, tar_code]:
            if code not in ["auto", "zh", "zh-cn", "zh-tw", "en"]:
                if settings.DEBUG_MODE:
                    print(
                        "I-Ciba can't translate languages %s -> %s" %
                        (src_code, tar_code))
                return None

        endpoint = "http://dict-co.iciba.com/api/dictionary.php"
        payload = {
            "w": source_text,
            "key": settings.ICIBA_API_KEY,
            "type": "json"
        }
        try:
            res = requests.get(endpoint, params=payload).json()
            for each in res.get("symbols", []):
                if each.get("parts"):
                    return res
            return None
        except Exception:
            if settings.DEBUG_MODE:
                raise
            return

    def display(self, result):
        symbols = result.get("symbols", [])
        for symbol in symbols:
            # phonetic
            for key in ["word_symbol", "ph_am", "ph_en"]:
                if key in symbol:
                    print("[%s]" % symbol[key])
                    break
            # meanings
            parts = symbol.get("parts", [])
            for part in parts:
                output = ""
                part_name = part.get("part_name", part.get("part"))
                if part_name:
                    output += "<%s> - " % part_name
                means = part.get("means", [])  # en -> zh
                if means:
                    if isinstance(means[0], dict):
                        means = list(
                            map(lambda m: m.get("word_mean", ""), means))
                    output += "; ".join(means)
                print(output)
