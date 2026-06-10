# Legal AI Contract Generator — Quick Start

> Generate professional legal contracts using AI. Five steps, under five minutes.

---

## Prerequisites

- Python 3.8+
- A [Google Gemini API key](https://makersuite.google.com/app/apikey) (free tier works)

---

## Setup

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd legal-ai

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create required directories
mkdir -p data/contracts data/embeddings data/outputs logs

# 5. Configure your API key
cp .env.example .env
# Open .env and set: GEMINI_API_KEY=your_key_here

# 6. Run
python -m src.legal_ai.main
```

---

## What Happens When You Run It

You'll be prompted to describe the contract you want:

```
Describe the contract you want:

> NDA between two tech companies covering IP and confidentiality
```

The app then runs five automated steps:

1. Converts your description into a structured legal specification
2. Searches your contract templates for relevant clauses (if any are loaded)
3. Drafts a full contract
4. Runs a legal review pass
5. Revises and saves the final document

Output is saved to `data/outputs/contract_YYYYMMDD_HHMMSS.docx`.

---

## Adding Contract Templates (Recommended)

The system works without templates but produces better results with them. Drop any `.txt` contract files into `data/contracts/`:

```bash
cp your_contracts/*.txt data/contracts/
```

Embeddings are cached after the first run, so subsequent runs are much faster.

---

## Configuration

All settings live in `.env`. Key options:

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required)* | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-pro` | Model to use |
| `JURISDICTION` | `England and Wales` | Legal jurisdiction |
| `RETRIEVAL_TOP_K` | `2` | Number of templates to retrieve |
| `CHUNK_SIZE` | `500` | Words per document chunk |
| `TEMPERATURE` | `0.2` | Generation creativity (0.0–1.0) |
| `DEBUG` | `true` | Verbose logging |

---

## Common Commands

```bash
python -m src.legal_ai.main     # Generate a contract
python tests/test_rag.py        # Test the retrieval system
pytest tests/                   # Run the full test suite
```

---

## Troubleshooting

**`ModuleNotFoundError`** — run `pip install -r requirements.txt` inside your virtual environment.

**API key error** — check `.env` contains `GEMINI_API_KEY=AIzaSy...` (not the placeholder).

**No templates found** — this is fine. Add `.txt` files to `data/contracts/` to improve output quality.

**Out of memory** — set `CHUNK_SIZE=250` in `.env`, then delete `data/embeddings/embeddings_cache.pkl`.

**Still stuck?** Check `logs/legal_ai_*.log` for the full error trace.