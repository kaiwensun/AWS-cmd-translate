import boto3, sys, os, importlib
import langdetect

import translators as Translators
from config import settings

translators_cache = {}

def clearScreen():
    command = "cls" if os.name=="nt" else "clear"
    os.system(command)

def search(source_text):
    success = False
    for engine_name in settings.ENGINES:
        try:
            if engine_name not in translators_cache:
                Translator = getattr(Translators, engine_name)
                translators_cache[engine_name] = Translator()
            translator = translators_cache[engine_name]
            res = translator.lookup(source_text)
            if res is None:
                continue
            translator.display(res)
            success = True
            if settings.ONLY_ONE_ENGINE:
                break
        except:
            if settings.DEBUG_MODE:
                raise
    if not success:
        print("Unable to translate.", file=sys.stderr)

def main():
    try:
        if len(sys.argv) > 1:
            line = " ".join(sys.argv[1:])
            search(line)
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
                    search(line)
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