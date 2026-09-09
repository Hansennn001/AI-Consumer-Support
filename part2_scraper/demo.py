from scraper import scrape_page
from cleaner import clean_html
from guardrail import limit_content
from summarizer import summarize



url = "https://example.com"


html = scrape_page(url)

cleaned = clean_html(html)

safe = limit_content(cleaned)

summary = summarize(safe)


print(summary)