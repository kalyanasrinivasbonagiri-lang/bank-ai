# BankAI

BankAI is a Flask-based banking guidance assistant that uses retrieval-augmented generation, OCR, and session-based chat to answer banking process questions from local documents. It is designed for guidance and education only. It is not a banking core system and does not access live accounts, balances, transactions, or personal customer data.

## Overview

BankAI is built for document-grounded banking assistance. It is best suited for questions such as:

- How to deposit money?
- What is the process for withdrawal?
- How to use ATM?
- How to check balance?
- How to fill a deposit slip?
- What is KYC?
- What documents are needed?

The assistant answers from indexed local source files and uploaded documents. When the required information is not available in the source material, it should respond honestly rather than inventing details.

## Key Features

- Flask application using the app factory pattern
- Modular package structure under `src/bank_ai/`
- Banking-specific routing for `general`, `rag`, `upload`, `summarize`, and `follow_up`
- Local RAG pipeline using Chroma
- Local Hugging Face embeddings with `sentence-transformers`
- OCR support for PDFs and images
- Groq integration for text generation and vision-based extraction
- Session-based chat memory
- Server-rendered Flask templates with a modern dark chat interface
- Scripts for setup verification and document indexing
- Basic tests for routes, sessions, RAG helpers, chat flow, and OCR text extraction

## Scope and Product Boundaries

BankAI is intentionally limited.

It can:

- explain banking processes from provided documents
- describe form fields in simple language
- summarize uploaded banking documents
- answer KYC and document guidance questions only when present in source material

It cannot:

- check live balances
- look up personal account information
- perform deposits, withdrawals, transfers, or transactions
- call real banking APIs
- invent RBI rules, cash limits, KYC policies, or bank-specific requirements

## Technology Stack

- Python 3.11+
- Flask 3.x
- Chroma
- LangChain
- Hugging Face embeddings
- Sentence Transformers
- Groq
- PyMuPDF
- Pillow
- Pytest
- `uv` for environment and dependency management

## Project Structure

```text
bank-ai/
├── app.py
├── wsgi.py
├── pyproject.toml
├── README.md
├── .env.example
├── data/
│   ├── raw/
│   ├── processed/
│   └── uploads/
├── storage/
│   ├── vector_db/
│   ├── logs/
│   └── cache/
├── docs/
├── scripts/
├── static/
├── templates/
└── src/bank_ai/
    ├── app_factory.py
    ├── config.py
    ├── extensions.py
    ├── constants/
    ├── llm/
    ├── ocr/
    ├── rag/
    ├── services/
    ├── schemas/
    ├── db/
    └── utils/
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd bank-ai
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create the environment file

```bash
copy .env.example .env
```

Update `.env` with your values, especially `GROQ_API_KEY`.

### 4. Add source documents

Place local banking guidance files inside `data/raw/`. Organize them by topic folders such as:

- `deposits/`
- `withdrawals/`
- `atm/`
- `balance/`
- `forms/`
- `kyc/`
- `rules/`
- `accounts/`

Supported indexing formats:

- `.txt`
- `.pdf`

Supported upload formats:

- `.txt`
- `.pdf`
- `.png`
- `.jpg`
- `.jpeg`

### 5. Build the vector index

```bash
uv run python scripts/index_data.py
```

### 6. Start the application

```bash
uv run app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Environment Variables

The project uses the following environment variables:

- `GROQ_API_KEY` - Groq API key for text and vision models
- `FLASK_SECRET_KEY` - Flask session secret
- `HOST` - Flask host, for example `127.0.0.1`
- `PORT` - Flask port, for example `5000`
- `LOG_LEVEL` - logging level such as `INFO`
- `SESSION_COOKIE_SECURE` - `true` or `false`

See [`.env.example`](/abs/path/c:/Users/kalya/Desktop/Bankai/.env.example) for the template.

## Example Workflow

1. Add banking guidance files to `data/raw/`
2. Run the indexing script
3. Start the Flask application
4. Ask a question such as `How to fill a deposit slip?`
5. Upload a PDF or image when document-specific guidance is needed

## Available Scripts

- `uv run python scripts/index_data.py`
  Builds the vector index from local source documents.

- `uv run python scripts/reindex_documents.py`
  Rebuilds the vector index.

- `uv run python scripts/verify_setup.py`
  Checks local directories and required setup state.

- `uv run pytest`
  Runs the test suite.

## Architecture Summary

### Frontend

- Flask server-rendered templates
- Dark minimal chat UI
- Session-rendered conversation history
- File upload form for OCR-supported documents

### Backend

- Flask app factory pattern
- Routing layer for web, API, admin, and health endpoints
- Service layer for chat orchestration, uploads, routing, responses, and session memory
- RAG pipeline for retrieval and document-grounded answers
- OCR layer for text extraction from files
- Groq wrapper for text and vision model interaction

## Example Questions

- How to deposit money?
- How to withdraw money from ATM?
- How to check balance?
- What is KYC?
- How to fill a deposit slip?
- What documents are needed for withdrawal?

## Development Notes

- The quality of answers depends on the quality of the indexed source material.
- Rules and policy answers should come only from available documents.
- If a source document does not contain the answer, BankAI should clearly say so.
- Local vector data, uploads, logs, and `.env` are excluded through `.gitignore`.

## Testing

Run the test suite with:

```bash
uv run pytest
```

The project includes basic coverage for:

- route behavior
- session handling
- query expansion and retrieval helpers
- chat service behavior
- text-file OCR extraction

## Repository Notes

If you plan to publish the project:

- keep `.env` out of version control
- review sample data before sharing publicly
- avoid storing private banking or customer information in `data/raw/` or `data/uploads/`

## License

Add your preferred license here before publishing.
