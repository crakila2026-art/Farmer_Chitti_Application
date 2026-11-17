
# 🌾 Farming Chitti – AI-Powered Farmer Assistant

## Project Overview

Farming Chitti is a multilingual AI agricultural
assistant designed to help farmers access
government agricultural scheme information.

## Key Features

1. Retrieval Augmented Generation (RAG)
2. Hybrid document search
3. Multilingual question answering
4. Tamil and English support
5. Evidence-grounded responses
6. Farmer profile management
7. Preliminary scheme eligibility assessment

## Technology Stack

- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS
- RAG
- Hybrid Search
- Pytest

## Project Architecture

Farmer Question
      |
      v
Language Detection
      |
      v
Query Rewriting
      |
      v
Multilingual Query Translation
      |
      v
Hybrid Retrieval
      |
      v
Government PDF Documents
      |
      v
LLM Answer Generation
      |
      v
Evidence Validation
      |
      v
Farmer Response

## Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate to the project:

cd farming-chitti

Create virtual environment:

python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Configure API key in .env.

Run application:

streamlit run conversation_app.py

## Testing

python -m pytest tests/ -v

## Evaluation

python -m evaluation.evaluator

## Project Status

Phase 8 – Quality and Delivery

## Disclaimer

Scheme eligibility results are preliminary.
Final eligibility is determined by the relevant
government department and applicable official rules.
