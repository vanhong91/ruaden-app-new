# check_localization.py
import logging
from ui import TEXT

logger = logging.getLogger(__name__)

def check_localization():
    """Check for missing translations in TEXT dictionary."""
    missing_keys = []
    english_keys = set(TEXT["English"].keys())
    vietnamese_keys = set(TEXT["Vietnamese"].keys())
    missing_in_vi = english_keys - vietnamese_keys
    for key in missing_in_vi:
        missing_keys.append(f"Missing Vietnamese translation for key: '{key}'")
        logger.error(f"Missing Vietnamese translation for key: '{key}'")
    missing_in_en = vietnamese_keys - english_keys
    for key in missing_in_en:
        missing_keys.append(f"Missing English translation for key: '{key}'")
        logger.error(f"Missing English translation for key: '{key}'")
    return not missing_keys, missing_keys

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success, errors = check_localization()
    if not success:
        print("Localization check failed with the following errors:")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("Localization check passed: All keys have translations.")