# AI Customer Support Agent

Agentic AI Customer Support System built using LangGraph, LangChain,
Gemini API, Tavily Search API, Retrieval-Augmented Generation (RAG), and
SQLite.

This project implements an AI customer support agent capable of
understanding customer requests, classifying issues, detecting risky
cases, escalating to human support, retrieving internal knowledge,
calling external tools, maintaining conversation memory, and logging
interactions.

------------------------------------------------------------------------

# 1. Project Overview

The system demonstrates an agentic AI workflow where multiple
specialized nodes collaborate through LangGraph state orchestration.

Main capabilities:

-   Customer request classification
-   Risk detection
-   Human-in-the-loop escalation
-   Internal knowledge retrieval (RAG)
-   External tool calling using Tavily
-   Conversation memory management
-   Conversation logging

------------------------------------------------------------------------

# 2. Features

## Request Classification

Customer requests are classified into:

-   refund
-   payment
-   security_breach
-   data_loss
-   service_outage
-   general

## Risk Detection and Human Escalation

Requests are escalated when:

-   Security breach is detected
-   Data loss is detected
-   Service outage is detected
-   Customer contacted support more than 3 times within 7 days

## Retrieval-Augmented Generation (RAG)

Standard customer support questions are answered using internal
knowledge.

Example:

Customer: "How long does refund take?"

Response: "Approved refunds will be processed within 5-7 business days."

## External Tool Decision

The agent decides whether external information is required.

Example:

Customer: "Is AWS experiencing downtime today?"

Flow:

Customer Request → Tool Decision → Tavily Search → Response Generation

## Conversation Memory

The system stores previous conversations and retrieves customer context
for future interactions.

Example:

Previous: "My name is Alex."

Next: "What is my name?"

The agent retrieves previous context from memory storage.

## Conversation Logging

The system stores:

-   customer ID
-   category
-   risk level
-   risk reason
-   response
-   escalation status
-   processing time

------------------------------------------------------------------------

# 3. System Architecture

    Customer Request

            |
            v

    Memory Retriever

            |
            v

    Classifier

            |
            v

    Risk Detector

            |
            +----------------+
            |                |
            v                v

    Human Review       Tool Decision

                             |
                  +----------+----------+
                  |                     |
                  v                     v

            Tavily Search          Knowledge Base

                  |                     |

                  +----------+----------+

                             |
                             v

                  Response Generator

                             |
                             v

                  Memory Saver

                             |
                             v

                        Logger

------------------------------------------------------------------------

# 4. Technology Stack

Backend: - Python - FastAPI

AI Framework: - LangChain - LangGraph

LLM: - Gemini API

External Search: - Tavily Search API

Database: - SQLite

Container: - Docker

------------------------------------------------------------------------

# 5. Project Structure

    customer-support-agent/

    ├── app/
    │   ├── agents/
    │   │   └── customer_agent.py
    │   │
    │   ├── nodes/
    │   │   ├── classifier.py
    │   │   ├── risk_detector.py
    │   │   ├── tool_decision.py
    │   │   ├── tavily_search.py
    │   │   ├── response_generator.py
    │   │   ├── memory_saver.py
    │   │   └── logger.py
    │   │
    │   ├── database/
    │   │   └── db.py
    │   │
    │   ├── api/
    │   │   └── main.py
    │   │
    │   └── testing/
    │       └── test_agent.py
    │
    ├── knowledge_base/
    ├── database/
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

# 6. Installation

Clone repository:

``` bash
git clone <repository-url>
cd customer-support-agent
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 7. Environment Configuration

Create environment file:

``` bash
cp .env.example .env
```

Required variables:

``` env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

------------------------------------------------------------------------

# 8. Running Application

Initialize database:

``` bash
python -m app.database.init
```

Run API:

``` bash
uvicorn app.api.main:app --reload
```

Application:

    http://localhost:8000

------------------------------------------------------------------------

# 9. API Endpoint

## Health Check

GET:

    /

Response:

``` json
{
  "status": "running",
  "message": "AI Customer Support Agent API"
}
```

## Customer Support Chat

POST:

    /chat

Example:

``` json
{
  "email": "My account was hacked"
}
```

------------------------------------------------------------------------

# 10. Testing

Run assessment validation:

``` bash
python -m app.testing.test_agent
```

Covered scenarios:

-   Security breach escalation
-   Data loss escalation
-   Service outage escalation
-   Customer contacted more than 3 times within 7 days
-   Refund knowledge retrieval
-   External tool decision
-   Conversation memory

Expected:

    7/7 TEST PASSED

------------------------------------------------------------------------

# 11. Docker Deployment

Build image:

``` bash
docker build -t customer-agent .
```

Run container:

``` bash
docker run --env-file .env -p 8000:8000 customer-agent
```

------------------------------------------------------------------------

# 12. Design Decisions

## Why LangGraph?

LangGraph provides explicit workflow orchestration, state management,
and conditional routing.

## Why Separate Classifier and Risk Detector?

Classifier determines the issue category.

Risk Detector determines whether human escalation is required.

This keeps responsibilities separated and easier to maintain.

## Why Use Tool Decision?

The LLM decides when external information is required instead of relying
on hardcoded keyword rules.

------------------------------------------------------------------------

# 13. Limitations

Current limitations:

-   SQLite is used for simplicity.
-   Authentication is not implemented.
-   Human review dashboard is not included.
-   External APIs depend on availability.
-   Production monitoring is not implemented.

------------------------------------------------------------------------

# 14. Future Improvements

Potential improvements:

-   PostgreSQL migration
-   Authentication and authorization
-   Human support dashboard
-   Advanced memory management
-   Additional tools
-   Monitoring and CI/CD pipeline

------------------------------------------------------------------------

# Validation Result

Current assessment validation:

    7/7 TEST PASSED

The system successfully demonstrates:

-   Agent workflow orchestration
-   Human escalation
-   RAG retrieval
-   Tool calling
-   Conversation memory
-   Logging