import boto3
import sys
import os
import importlib
import langdetect

import translators as Translators
from config import settings

translators_cache = {}


def clearScreen():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def snake2camel(name):
    return "".join(map(str.capitalize, name.split("_")))


def embed_word_in_line(word, length=30, line_char="="):
    left_len = max(0, (length - len(word)) // 2 - 1)
    right_len = max(0, length - len(word) - left_len - 1)
    return line_char * left_len + " " + word + " " + line_char * right_len


def search(source_text):
    if not source_text.strip():
        return
    success = False
    for engine_name in settings.ENGINES:
        try:
            if engine_name not in translators_cache:
                Translator = getattr(
                    getattr(
                        Translators,
                        engine_name),
                    snake2camel(engine_name))
                translators_cache[engine_name] = Translator()
            translator = translators_cache[engine_name]
            if settings.DEBUG_MODE or settings.DISPLAY_SOURCE_DICT:
                print(embed_word_in_line(engine_name))
            res = translator.lookup(source_text)
            if res is None:
                continue
            translator.display(res)
            success = True
            if settings.ONLY_ONE_ENGINE:
                break
        except Exception:
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
                    if line == 'exit':
                        break
                    if line == 'clear' or line == 'cls':
                        clearScreen()
                        continue
                    if len(line) == 0:
                        continue
                    search(line)
                except (EOFError, KeyboardInterrupt):
                    break
                except Exception:
                    if settings.DEBUG_MODE:
                        raise
                    print("An error occured.", file=sys.stderr)
    except Exception:
        if settings.DEBUG_MODE:
            raise
        print("An error occured.", file=sys.stderr)


if __name__ == "__main__":
    main()
