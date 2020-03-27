import boto3
import sys
import os
import langdetect
import functools
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

    def lookup(self, source_text, src_code, tar_code):
        src_code = self._iso639_to_amazon_code(src_code)
        tar_code = self._iso639_to_amazon_code(tar_code)
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

    def _iso639_to_amazon_code(self, code):
        if code is None or code == "auto":
            return code
        if code == "zh-cn":
            code = "zh"
        if code.lower() == "zh-tw":
            code = "zh-TW"
        else:
            code = code.split("-")[0]
        if code not in settings.AWS_SUPPORTED_LANGUAGES:
            if settings.DEBUG_MODE:
                raise Exception(
                    "Amazon Translate doesn't support language %s" %
                    code)
        return code
