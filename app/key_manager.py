import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


ENV_PATH = os.path.join(
    BASE_DIR,
    ".env"
)


print("Loading ENV from:")
print(ENV_PATH)


loaded = load_dotenv(
    ENV_PATH,
    override=True
)


print("dotenv loaded:", loaded)


print("RAW ENV CHECK:")
print(os.environ.get("GEMINI_API_KEY_1"))


API_KEYS = [
    os.environ.get("GEMINI_API_KEY_1"),
    os.environ.get("GEMINI_API_KEY_2"),
    os.environ.get("GEMINI_API_KEY_3"),
    os.environ.get("GEMINI_API_KEY_4"),
    os.environ.get("GEMINI_API_KEY_5"),
    os.environ.get("GEMINI_API_KEY_6"),
    os.environ.get("GEMINI_API_KEY_7")
]


print("\nKEY STATUS:")

for key in API_KEYS:
    if key:
        print(
            "FOUND:",
            key[:10]
        )
    else:
        print(
            "EMPTY"
        )


index = 0


def get_next_key():

    global index

    key = API_KEYS[index]

    index += 1

    if index >= len(API_KEYS):
        index = 0

    return key