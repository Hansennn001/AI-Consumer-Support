import re

from bs4 import BeautifulSoup


REMOVE_TAGS = [
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    "noscript",
    "svg",
    "form"
]


def clean_html(html: str) -> str:
    """
    Remove HTML noise and keep meaningful content.
    """

    if not html:
        return ""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup.find_all(REMOVE_TAGS):
        tag.decompose()

    # Prefer semantic article/main content
    content = (
        soup.find("article")
        or soup.find("main")
        or soup.body
        or soup
    )

    text = content.get_text(
        separator="\n",
        strip=True
    )

    # Normalize excessive whitespace
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text.strip()