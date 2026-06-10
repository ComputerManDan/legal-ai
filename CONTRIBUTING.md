# Contributing

## Getting Started

```bash
git clone <repo-url>
cd legal-ai
python -m venv venv
source venv/bin/activate
make install-dev
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

## Project Structure

```
legal-ai/
├── src/legal_ai/
│   ├── main.py         # Entry point and generation pipeline
│   ├── rag.py          # Retrieval-augmented generation (embeddings + search)
│   ├── config.py       # All configuration, loaded from .env
│   ├── logger.py       # Logging setup
│   └── utils/
│       └── validators.py
├── tests/
│   └── test_rag.py
├── data/
│   ├── contracts/      # Add .txt contract templates here
│   ├── embeddings/     # Auto-generated embedding cache
│   └── outputs/        # Generated .docx contracts
├── logs/
├── .env.example        # Copy to .env and fill in your key
├── Makefile
├── requirements.txt
└── requirements-dev.txt
```

## Workflow

1. Create a branch: `git checkout -b your-feature`
2. Make your changes in `src/legal_ai/`
3. Add or update tests in `tests/`
4. Run `make test` and `make lint` — both must pass
5. Open a pull request with a clear description of what changed and why

## Code Style

- Formatter: `black` (line length 100) — run `make format`
- Linter: `flake8` — run `make lint`
- Type hints are encouraged but not required

## Testing

```bash
make test-rag   # Quick smoke test for the retrieval system
make test       # Full pytest suite
```

Tests do not require a real API key. The RAG tests run against whatever is in `data/contracts/` (empty is fine — it just skips retrieval tests).

## Environment Variables

Never commit `.env`. It's in `.gitignore`. Use `.env.example` to document any new variables you add.

## Key Design Decisions

**RAG caching** — embeddings are pickled to `data/embeddings/` after first generation. If you change the documents or embedding model, delete the cache with `make clear-cache`.

**Retry logic** — Gemini API calls use `tenacity` with exponential backoff (3 attempts, 4–10s wait). Don't remove this; the API rate-limits aggressively.

**Config as a class** — all env vars live in `config.py` as class attributes. Add new settings there rather than calling `os.getenv()` directly in other modules.
