# BankAI

BankAI is a banking guidance assistant built with Flask, RAG, OCR, session-based chat, Chroma, and Groq. It answers banking process questions from local documents and uploaded files. It does not connect to any bank account or live banking system.

## What BankAI Does

- Explains deposit and withdrawal processes
- Guides ATM usage and balance-check steps
- Explains banking forms and common fields
- Answers KYC and document requirement questions only from source material
- Summarizes uploaded banking documents when relevant

## What BankAI Does Not Do

- No live balance checking
- No account lookup
- No transactions
- No personal banking API actions
- No invented banking rules or RBI policies

## Quickstart

1. Install dependencies:

```bash
uv sync
```

2. Create your environment file:

```bash
copy .env.example .env
```

3. Add local banking guidance documents under `data/raw/`

4. Build the local vector index:

```bash
uv run python scripts/index_data.py
```

5. Start the app:

```bash
uv run app.py
```

6. Open the browser at `http://127.0.0.1:5000`

## Project Layout

```text
bank-ai/
├── app.py
├── wsgi.py
├── pyproject.toml
├── README.md
├── .env.example
├── data/
├── docs/
├── scripts/
├── static/
├── templates/
└── src/bank_ai/
```

## Environment Variables

- `GROQ_API_KEY`
- `FLASK_SECRET_KEY`
- `HOST`
- `PORT`
- `LOG_LEVEL`
- `SESSION_COOKIE_SECURE`

## Sample Questions

- How to deposit money?
- What is the process for withdrawal?
- How to withdraw money from ATM?
- How to check balance?
- How to fill a deposit slip?
- What is KYC?
- What documents are needed?

## Development

- Use `uv run pytest` to run tests
- Use `uv run python scripts/verify_setup.py` to check the local setup
- Use `uv run python scripts/reindex_documents.py` to rebuild the index

## Notes

BankAI is only as strong as the local source documents you provide. If a rule or process is not present in the indexed documents, BankAI should say that the information is unavailable in the source material.
