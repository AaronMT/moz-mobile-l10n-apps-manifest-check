import json
import sys


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def check_missing_locales(shipping_locales, apk_locales):
    missing_locales = [locale for locale in shipping_locales if locale not in apk_locales]
    return missing_locales


if __name__ == "__main__":
    shipping_locales_path = 'shipping_locales.json'
    apk_locales_path = 'apk_locales.json'

    try:
        shipping_locales = load_json(shipping_locales_path)
        apk_locales = load_json(apk_locales_path)
        
        missing_locales = check_missing_locales(shipping_locales, apk_locales)
        
        if missing_locales:
            print(f"Missing locales: {missing_locales}")
            sys.exit(1)
        else:
            print("All locales are present.")
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
