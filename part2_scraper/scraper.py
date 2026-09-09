import requests


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; AgenticArchitectChallenge/1.0)"
    )
}


def scrape_page(url: str) -> str:
    """
    Retrieve raw HTML from a webpage.
    """

    if not url.startswith(("http://", "https://")):
        raise ValueError(
            "URL must start with http:// or https://"
        )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Failed to retrieve webpage: {exc}"
        ) from exc