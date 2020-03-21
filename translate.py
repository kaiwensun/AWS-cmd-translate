import boto3, sys, os
import langdetect
from config import settings

AWS_CLIENT_CONFIG = {
    "region_name": settings.AWS_REGION_NAME,
    "api_version": settings.AWS_API_VERSION,
    "endpoint_url": settings.AWS_ENDPOINT_URL,
    "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
    "aws_session_token": settings.AWS_SESSION_TOKEN
}
translate_client = boto3.client('translate', **AWS_CLIENT_CONFIG)

def langdetect2aws(code):
    if code == "zh-cn":
        return "zh"
    if code == "zh-tw":
        return "zh-TW"
    s = code.split("-")
    if len(s) == 2:
        return "-".join((s[0], s[1].upper()))
    return code

def lookup(source_text):
    src_code = langdetect.detect(source_text)
    src_code = langdetect2aws(src_code)
    tar_code = "en"
    if src_code in settings.AWS_NOT_SUPPORTED_LANGUAGES:
        if settings.DEBUG_MODE:
            print("%s language is detected but not supported. use aws auto." % src_code)
        src_code = "auto"
        tar_code = settings.MAIN_LANGUAGE
    else:
        if src_code[:2] == settings.MAIN_LANGUAGE[:2]:
            tar_code = "zh" if src_code == "en" else "en"
        else:
            tar_code = settings.MAIN_LANGUAGE
    result = translate_client.translate_text(Text=source_text, SourceLanguageCode=src_code, TargetLanguageCode=tar_code)
    if settings.DEBUG_MODE:
        print("(%s -> %s)" % (src_code, tar_code))
        import pprint
        pprint.pprint(result)

    translated_text = result['TranslatedText']
    display(translated_text)

def display(translated_text):
    print(translated_text)

def clearScreen():
    command = "cls" if os.name=="nt" else "clear"
    os.system(command)

def main():
    try:
        if len(sys.argv) > 1:
            word = " ".join(sys.argv[1:])
            lookup(word)
        else:
            while True:
                try:
                    line = input("> ")
                    if line=='exit':
                        break
                    if line=='clear' or line=='cls':
                        clearScreen()
                        continue
                    if len(line)==0:
                        continue
                    lookup(line)
                except (EOFError,KeyboardInterrupt):
                    break
                except:
                    if settings.DEBUG_MODE:
                        raise
                    print("An error occured.", file=sys.stderr)
    except:
        if settings.DEBUG_MODE:
            raise
        print("An error occured.", file=sys.stderr)

if __name__ == "__main__":
    main()