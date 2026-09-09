import argparse

from part2_scraper.scraper import (
    scrape_page
)

from part2_scraper.cleaner import (
    clean_html
)

from part2_scraper.summarizer import (
    summarize_text
)


def run_pipeline(
    url: str,
    llm=None
) -> str:

    html = scrape_page(
        url
    )

    cleaned = clean_html(
        html
    )

    if not cleaned:
        return (
            "No meaningful content was found "
            "on the webpage."
        )

    return summarize_text(
        cleaned,
        llm=llm
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Scrape and summarize "
            "a webpage."
        )
    )

    parser.add_argument(
        "url",
        help="Public webpage URL"
    )

    args = parser.parse_args()

    try:

        summary = run_pipeline(
            args.url
        )

        print(
            "\n============================"
        )

        print(
            "FINAL CONCISE SUMMARY"
        )

        print(
            "============================"
        )

        print(
            summary
        )

    except Exception as exc:

        print(
            f"\nPipeline failed: {exc}"
        )


if __name__ == "__main__":
    main()