import boto3
import sys
import os
import langdetect
from config import settings


class AmazonTranslate:

    def __init__(self):
        config = {
            "region_name": settings.AWS_REGION_NAME,
            "api_version": settings.AWS_API_VERSION,
            "endpoint_url": settings.AWS_ENDPOINT_URL,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "aws_session_token": settings.AWS_SESSION_TOKEN
        }
        self._translate_client = boto3.client('translate', **config)

    def _langdetect2aws(self, code):
        if code == "zh-cn":
            return "zh"
        if code == "zh-tw":
            return "zh-TW"
        s = code.split("-")
        if len(s) == 2:
            return "-".join((s[0], s[1].upper()))
        return code

    def lookup(self, source_text):
        src_code = langdetect.detect(source_text)
        src_code = self._langdetect2aws(src_code)
        tar_code = "en"
        if src_code in settings.AWS_NOT_SUPPORTED_LANGUAGES:
            if settings.DEBUG_MODE:
                print("%s language is detected but not supported."
                      " use aws auto." % src_code)
            src_code = "auto"
            tar_code = settings.MAIN_LANGUAGE
        else:
            if src_code[:2] == settings.MAIN_LANGUAGE[:2]:
                tar_code = "zh" if src_code == "en" else "en"
            else:
                tar_code = settings.MAIN_LANGUAGE
        result = self._translate_client.translate_text(
            Text=source_text,
            SourceLanguageCode=src_code,
            TargetLanguageCode=tar_code)
        if settings.DEBUG_MODE:
            print("(%s -> %s)" % (src_code, tar_code))
            import pprint
            pprint.pprint(result)

        return result['TranslatedText']

    def display(self, translation_result):
        print(translation_result)
