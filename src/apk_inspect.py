import argparse
import json
import subprocess


def is_aapt_available():
    try:
        result = subprocess.run(["aapt", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_locales_from_apk(apk_path):
    try:
        result = subprocess.run(["aapt", "dump", "badging", apk_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Error running aapt: {result.stderr}")

        for line in result.stdout.splitlines():
            if "locales:" in line:
                return line.split("locales:")[1].strip().split("'")[1::2]

        return []
    except Exception as e:
        raise Exception(f"Error getting locales from APK: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract locales from APK using aapt.")
    parser.add_argument("apk_path", help="Path to the APK file")
    args = parser.parse_args()

    if not is_aapt_available():
        print("Error: aapt tool is not available. Please ensure the Android SDK is installed and aapt is in your PATH.")
        exit(1)

    try:
        locales = get_locales_from_apk(args.apk_path)
        with open("apk_locales.json", "w") as json_file:
            json.dump(locales, json_file)
        print("Locales have been written to apk_locales.json")
    except Exception as e:
        print(e)
