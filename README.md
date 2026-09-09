# AI Customer Support Agent

## Project Overview

Brief project explanation.

## Components

### Part 1-3: Agentic AI Customer Support System

- LangGraph workflow
- Classification
- Risk detection
- Human escalation
- RAG
- Tavily tool
- Memory
- Logging
  
## Architecture
<img width="529" height="1263" alt="Architecture" src="https://github.com/user-attachments/assets/1103ec1e-204d-40d2-80e5-254df25a3fc7" />


### Part 2: Web Scraping & Summarization Pipeline

- HTML extraction
- Cleaning
- Chunking
- Gemini summarization
- Output guardrail


## Architecture
<img width="172" height="752" alt="architecturepart2" src="https://github.com/user-attachments/assets/ac46a9e3-7cf4-44a7-8bdd-f19596965e95" />

## Technology Stack

- Python
- LangGraph
- LangChain
- Gemini API
- Tavily
- FastAPI
- SQLite
- Docker

## Testing

Part 1:
7/7 passed

Part 2:
5/5 passed

# Local Environment Setup

## Requirements

Before running the project, ensure the following are installed:

- Python 3.10+
- pip
- Docker (optional)

---

## 1. Clone Repository

```bash
git clone <repository-url>

cd customer-support-agent
````

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```
---

## 4. Configure API Keys

Create environment file:

```bash
cp .env.example .env
```

Required environment variables:

```env
GEMINI_API_KEY_1=your_gemini_api_key
GEMINI_API_KEY_2=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The application uses Gemini API for LLM processing and Tavily API for external search.

---

## 5. Initialize Database

Run:

```bash
python -m app.database.init
```

The system uses SQLite for local development.

---

## 6. Run Application

Start FastAPI server:

```bash
uvicorn app.api.main:app --reload
```

API available at:

```
http://localhost:8000
```

---

## 7. Run Tests

Run AI Customer Support Agent tests:

```bash
pytest app/testing/test_agent.py -v
```

Run scraper pipeline tests:

```bash
pytest part2_scraper/tests/test_pipeline.py -v -s
```

Expected:

```
Part 1:
7/7 tests passed

Part 2:
5/5 tests passed
```

---

## 8. Docker Execution (Optional)

Build image:

```bash
docker build -t customer-agent .
```

Run container:

```bash
docker run --env-file .env -p 8000:8000 customer-agent
```

```

---


## Documentation

Detailed documentation:
- Part 1-3 documentation `app/README.md`
- Part 2 pipeline: `part2_scraper/README.md`
