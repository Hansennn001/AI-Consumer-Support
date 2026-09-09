# Part 2 - Web Scraping & Summarization Pipeline

## Overview

This module implements a web scraping and AI-powered summarization pipeline.

The objective of this component is to solve webpage summarization challenges caused by:

- noisy HTML structures
- irrelevant webpage elements
- large webpage content exceeding LLM context limitations

The pipeline extracts meaningful webpage content, removes unnecessary information, processes long documents efficiently, and generates concise summaries using Gemini API.

---

# Pipeline Architecture

```

Web URL

|

v

HTML Scraper

|

v

HTML Cleaner

|

v

Content Chunking

|

v

Gemini Summarization

|

v

Output Guardrail

|

v

Final Summary

```

---

# Components

## 1. Web Scraper

File:

```

scraper.py

```

Responsible for retrieving webpage HTML content.

Implemented handling:

- URL validation
- HTTP request timeout
- HTTP status validation
- Network error handling


The scraper only retrieves raw content. Processing and filtering are handled by the following pipeline stages.

---

## 2. HTML Cleaner

File:

```

cleaner.py

```

Raw webpages often contain unnecessary elements that reduce summarization quality.

The cleaner removes:

- script tags
- style tags
- navigation menus
- headers
- footers
- forms
- metadata elements


Example:

Before:

```

Navigation
Advertisement
Article Content
Footer

```


After:

```

Article Content

```


This reduces unnecessary tokens before sending content to the LLM.

---

## 3. Long Content Processing

File:

```

guardrail.py

```

Large webpages may exceed LLM context limitations.

To handle this problem, the pipeline implements chunk-based processing.

Flow:

```

Large Document

```
  |

  v
```

Multiple Content Chunks

```
  |

  v
```

Individual Summaries

```
  |

  v
```

Final Summary

```


Benefits:

- prevents context overflow
- improves reliability
- supports longer documents
- maintains important information coverage

---

## 4. Gemini Summarization

File:

```

summarizer.py

```

The summarizer uses Gemini API to generate concise summaries from cleaned webpage content.


The summarization prompt enforces:

- factual information only
- no unsupported assumptions
- duplicate information removal
- concise bullet format


For long documents, the pipeline applies a map-reduce style approach:

```

Chunk 1  ---> Summary 1
Chunk 2  ---> Summary 2
Chunk 3  ---> Summary 3

```
          |

          v

  Final Consolidated Summary
```

````

---

## 5. Output Guardrail

The final response is controlled to ensure consistent output quality.

Rules:

- maximum 5 bullet points
- maximum summary length
- concise response format


This prevents uncontrolled LLM output and improves usability.

---

# Testing

The pipeline is validated using automated tests.

Test coverage:

1. Complex HTML cleaning
2. Long content chunking
3. Summary output guardrail
4. LLM summarization workflow
5. Complete end-to-end pipeline execution


Run:

```bash
pytest part2_scraper/tests/test_pipeline.py -v -s
````

Expected result:

```
5 passed
```

The automated tests use an LLM abstraction to ensure deterministic validation without depending on external API availability or quota.

Production execution still uses Gemini API.

---

# Running the Pipeline

Run the real Gemini summarization pipeline:

```bash
python -m part2_scraper.main <URL>
```

Example:

```bash
python -m part2_scraper.main https://www.ibm.com/topics/artificial-intelligence
```

Example output:

```
FINAL CONCISE SUMMARY

- Artificial intelligence enables machines to simulate human intelligence.
- Generative AI uses foundation models to create new content.
- AI provides benefits across multiple industries.
- AI implementation requires responsible governance.
- AI development continues to evolve rapidly.
```

---

# Design Decisions

## Why Clean HTML Before LLM Processing?

Sending raw HTML directly to an LLM introduces unnecessary information such as scripts, navigation, and metadata.

Cleaning improves:

* token efficiency
* summarization accuracy
* processing reliability

---

## Why Use Chunk-Based Processing?

Large documents may exceed LLM context limitations.

Chunking provides scalability while preserving important information from longer webpages.

---

## Why Use Gemini API?

Gemini provides strong language understanding capabilities required for extracting and summarizing webpage information.

---

# Limitations

Current limitations:

* JavaScript-heavy websites are not rendered
* No distributed crawling system
* Summary quality depends on LLM availability

Potential improvements:

* Playwright-based browser rendering
* asynchronous crawling
* advanced document ranking
* vector-based retrieval

---

# Validation Result

Final validation:

```
5/5 test cases passed
```

The pipeline successfully demonstrates:

* webpage extraction
* HTML noise removal
* long-document handling
* LLM-based summarization
* output quality control

```

---