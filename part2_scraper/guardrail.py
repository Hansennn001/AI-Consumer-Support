import re
from typing import List


MAX_CHUNK_CHARS = 8000
MAX_SUMMARY_BULLETS = 5
MAX_SUMMARY_CHARS = 1200


def chunk_content(
    text: str,
    max_chars: int = MAX_CHUNK_CHARS
) -> List[str]:

    if not text:
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        # One very large paragraph
        if len(paragraph) > max_chars:

            if current:
                chunks.append(
                    current.strip()
                )
                current = ""

            for start in range(
                0,
                len(paragraph),
                max_chars
            ):
                chunks.append(
                    paragraph[
                        start:start + max_chars
                    ]
                )

            continue

        candidate = (
            f"{current}\n{paragraph}"
            if current
            else paragraph
        )

        if len(candidate) <= max_chars:

            current = candidate

        else:

            if current:
                chunks.append(
                    current.strip()
                )

            current = paragraph

    if current:
        chunks.append(
            current.strip()
        )

    return chunks


def enforce_summary_guardrail(
    summary: str
) -> str:
    """
    Maximum 5 bullet points
    and maximum 1200 characters.
    """

    if not summary:
        return ""

    lines = [
        line.strip()
        for line in summary.splitlines()
        if line.strip()
    ]

    bullets = []

    for line in lines:

        if line.startswith(
            ("-", "*", "•")
        ):

            content = line.lstrip(
                "-*• "
            ).strip()

            if content:
                bullets.append(
                    f"- {content}"
                )

    # LLM sometimes ignores bullet instruction
    if not bullets:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            summary.strip()
        )

        bullets = [
            f"- {sentence.strip()}"
            for sentence in sentences
            if sentence.strip()
        ]

    bullets = bullets[
        :MAX_SUMMARY_BULLETS
    ]

    result = "\n".join(
        bullets
    )

    if len(result) > MAX_SUMMARY_CHARS:

        result = result[
            :MAX_SUMMARY_CHARS
        ].rstrip()

    return result