from part2_scraper.cleaner import (
    clean_html
)

from part2_scraper.guardrail import (
    chunk_content,
    enforce_summary_guardrail,
    MAX_CHUNK_CHARS,
    MAX_SUMMARY_BULLETS,
    MAX_SUMMARY_CHARS
)

from part2_scraper.summarizer import (
    summarize_text
)

from part2_scraper import main as pipeline


class FakeResponse:

    def __init__(
        self,
        content
    ):
        self.content = content


class FakeLLM:

    def __init__(self):
        self.calls = 0

    def invoke(
        self,
        prompt
    ):

        self.calls += 1

        return FakeResponse(
            """
- Artificial intelligence improves customer support.
- AI agents automate customer communication.
- Memory maintains conversational context.
- Retrieval provides relevant information.
- Guardrails improve system reliability.
- This point must be removed.
- This point must also be removed.
"""
        )


def test_complex_html_cleaning():

    html = """
<html>

<head>

<script>
analytics_tracking()
</script>

<style>
body { color: red; }
</style>

</head>

<body>

<nav>
Home About Contact Login
</nav>

<article>

<h1>
AI Customer Support System
</h1>

<p>
Artificial intelligence improves
customer support workflows.
</p>

</article>

<footer>
Copyright 2026
</footer>

</body>
</html>
"""

    cleaned = clean_html(
        html
    )

    print(
        "\n========== CLEANED =========="
    )

    print(cleaned)

    assert (
        "AI Customer Support System"
        in cleaned
    )

    assert (
        "analytics_tracking"
        not in cleaned
    )

    assert (
        "Copyright"
        not in cleaned
    )


def test_long_content_chunking():

    content = (
        (
            "Artificial intelligence "
            "improves customer support "
            "operations.\n"
        )
        * 1000
    )

    chunks = chunk_content(
        content
    )

    print(
        "\n========== CHUNKING =========="
    )

    print(
        "Original length:",
        len(content)
    )

    print(
        "Chunks:",
        len(chunks)
    )

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"Chunk {index}: "
            f"{len(chunk)} chars"
        )

    assert len(chunks) > 1

    assert all(
        len(chunk)
        <= MAX_CHUNK_CHARS
        for chunk in chunks
    )


def test_summary_guardrail():

    result = (
        enforce_summary_guardrail(
            """
- Point one.
- Point two.
- Point three.
- Point four.
- Point five.
- Point six.
- Point seven.
"""
        )
    )

    print(
        "\n========== GUARDED SUMMARY =========="
    )

    print(result)

    bullets = [
        line
        for line in result.splitlines()
        if line.startswith("- ")
    ]

    assert (
        len(bullets)
        <= MAX_SUMMARY_BULLETS
    )

    assert (
        len(result)
        <= MAX_SUMMARY_CHARS
    )

    assert (
        "Point six"
        not in result
    )


def test_long_content_summarization():

    fake_llm = FakeLLM()

    content = (
        (
            "Artificial intelligence improves "
            "customer support. "
            "AI agents can use memory, "
            "retrieval, and tools.\n"
        )
        * 1000
    )

    result = summarize_text(
        content,
        llm=fake_llm
    )

    print(
        "\n========== SUMMARY =========="
    )

    print(result)

    print(
        "LLM calls:",
        fake_llm.calls
    )

    assert fake_llm.calls > 1

    assert (
        len(result)
        <= MAX_SUMMARY_CHARS
    )


def test_complete_pipeline(
    monkeypatch
):

    fake_llm = FakeLLM()

    html = """
<html>

<head>

<script>
tracking()
</script>

</head>

<body>

<nav>
Home Products Login
</nav>

<article>

<h1>
Agentic AI Architecture
</h1>

<p>
AI agents can automate
customer support workflows.
</p>

<p>
Reliable systems use memory,
retrieval, tools,
and human escalation.
</p>

</article>

<footer>
Copyright
</footer>

</body>

</html>
"""

    # Only network request is mocked.
    # Cleaner, summarizer and guardrail
    # are real production functions.

    monkeypatch.setattr(
        pipeline,
        "scrape_page",
        lambda url: html
    )

    result = pipeline.run_pipeline(
        "https://example.com",
        llm=fake_llm
    )

    print(
        "\n========== FULL PIPELINE =========="
    )

    print(result)

    assert result

    assert (
        fake_llm.calls >= 1
    )

    assert (
        len(result)
        <= MAX_SUMMARY_CHARS
    )