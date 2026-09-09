import os
import logging

from dotenv import load_dotenv


# ======================================================
# LOGGER
# ======================================================

logger = logging.getLogger(__name__)


# ======================================================
# LOAD ENVIRONMENT
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


ENV_PATH = os.path.join(
    BASE_DIR,
    ".env"
)


load_dotenv(
    ENV_PATH,
    override=True
)


# ======================================================
# GEMINI API KEYS
# ======================================================

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
    os.getenv("GEMINI_API_KEY_6"),
    os.getenv("GEMINI_API_KEY_7"),
]


# Remove empty keys

API_KEYS = [
    key
    for key in API_KEYS
    if key
]


if API_KEYS:

    logger.info(
        "Gemini API providers loaded: %s",
        len(API_KEYS)
    )

else:

    logger.warning(
        "No Gemini API key configured."
    )



# ======================================================
# KEY ROTATION
# ======================================================

_current_index = 0



def get_next_key():

    """
    Return next available Gemini API key.

    Used for fallback rotation when
    previous provider fails.
    """

    global _current_index


    if not API_KEYS:

        raise RuntimeError(
            "No Gemini API key available."
        )


    key = API_KEYS[
        _current_index
    ]


    _current_index += 1


    if _current_index >= len(API_KEYS):

        _current_index = 0


    return key