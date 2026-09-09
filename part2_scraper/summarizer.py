from typing import Optional

from app.llm import get_llm_with_fallback

from part2_scraper.guardrail import (
    chunk_content,
    enforce_summary_guardrail
)


def invoke_llm(
    llm,
    prompt: str
) -> str:

    result = llm.invoke(
        prompt
    )

    if hasattr(result, "content"):
        return str(
            result.content
        ).strip()

    return str(result).strip()


def summarize_text(
    text: str,
    llm: Optional[object] = None
) -> str:
    """
    Summarize cleaned webpage content.

    Runtime:
    llm=None -> real Gemini

    Automated tests:
    llm=FakeLLM -> deterministic test double
    """

    if not text.strip():

        return (
            "No meaningful content was found "
            "on the webpage."
        )

    # THIS IS THE REAL GEMINI CONNECTION
    if llm is None:
        llm = get_llm_with_fallback()

    chunks = chunk_content(
        text
    )

    if not chunks:
        return (
            "No meaningful content was found "
            "on the webpage."
        )

    partial_summaries = []

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        prompt = f"""
You are a webpage summarization assistant.

Summarize the content below accurately.

Rules:
- Use only facts contained in the provided content.
- Do not invent information.
- Ignore advertisements or irrelevant website elements.
- Keep only important information.
- Maximum 5 concise bullet points.
- Do not include introductory commentary.

Content chunk {index}/{len(chunks)}:

{chunk}
"""

        partial = invoke_llm(
            llm,
            prompt
        )

        partial = (
            enforce_summary_guardrail(
                partial
            )
        )

        partial_summaries.append(
            partial
        )

    # Short page = one Gemini request
    if len(partial_summaries) == 1:
        return partial_summaries[0]

    # Long page:
    # summarize each chunk, then summarize summaries
    combined = "\n\n".join(
        partial_summaries
    )

    final_prompt = f"""
Create one final concise summary from
the partial summaries below.

Rules:
- Maximum 5 bullet points.
- Keep only the most important facts.
- Remove duplicate information.
- Do not invent information.
- Do not mention chunks or processing.
- Do not include introductory commentary.

Partial summaries:

{combined}
"""

    final_summary = invoke_llm(
        llm,
        final_prompt
    )

    return enforce_summary_guardrail(
        final_summary
    )