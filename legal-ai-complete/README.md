# Legal AI Contract Generator

An AI-powered legal contract generator using RAG (Retrieval-Augmented Generation) and Google Gemini API.

## Features

- ✅ **Smart Retrieval**: Cosine similarity-based RAG with embedding caching
- ✅ **Reliable**: Automatic retry logic with exponential backoff
- ✅ **Validated**: Input validation and comprehensive error handling
- ✅ **Efficient**: Embedding caching for 50-100x speedup
- ✅ **Observable**: Comprehensive logging to file and console
- ✅ **Configurable**: Centralized config with environment variables
- ✅ **Professional**: Enterprise-grade contract generation

## Project Structure

```
legal-ai/
├── src/legal_ai/              # Source code package
│   ├── main.py               # Main application entry point
│   ├── rag.py                # RAG retrieval module
│   ├── config.py             # Centralized configuration
│   ├── logger.py             # Logging setup
│   └── utils/
│       └── validators.py      # Input validation utilities
│
├── tests/                     # Test suite
│   ├── test_rag.py
│   └── fixtures/              # Test data
│
├── data/                      # Data directory
│   ├── contracts/             # Contract templates (add .txt files here)
│   ├── embeddings/            # Cached embeddings
│   └── outputs/               # Generated contracts
│
├── logs/                      # Application logs
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── Makefile                   # Common commands
└── README.md                  # This file
```

## Quick Start

### 1. Clone and Setup
```bash
cd legal-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
make setup
```

### 2. Configure
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env with your Gemini API key
GEMINI_API_KEY=your_key_here
```

### 3. Add Contract Templates
Place your contract templates (.txt files) in the `data/contracts/` directory.

### 4. Generate a Contract
```bash
make run
```

## Usage

### Generate a Contract
```bash
python -m src.legal_ai.main
```

This will:
1. Prompt you to describe the contract you want
2. Generate a structured legal specification
3. Retrieve relevant clauses from your contract templates
4. Draft an initial contract
5. Review and revise the contract
6. Save to `data/outputs/contract_YYYYMMDD_HHMMSS.docx`

### Test RAG Retrieval
```bash
make test-rag
```

### View Logs
```bash
make logs
```

### Run Tests
```bash
make test
```

## Configuration

Edit `.env` to customize:

```env
# Gemini API
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-pro

# Generation
TEMPERATURE=0.2
MAX_OUTPUT_TOKENS=8192

# Retrieval
RETRIEVAL_TOP_K=2
CHUNK_SIZE=500

# Other
JURISDICTION=England and Wales
DEBUG=true
```

## Output Files

Generated contracts are saved with timestamps:
- **Contracts**: `data/outputs/contract_YYYYMMDD_HHMMSS.docx`
- **Logs**: `logs/legal_ai_YYYYMMDD.log`
- **Cache**: `data/embeddings/embeddings_cache.pkl`

## Troubleshooting

### No contracts found
- Ensure .txt files are in `data/contracts/`
- Check logs: `tail logs/legal_ai_*.log`

### API key error
- Verify `GEMINI_API_KEY` is set in `.env`
- Don't commit `.env` (it's in `.gitignore`)

### Out of memory
- Reduce `CHUNK_SIZE` in `.env`
- Delete `data/embeddings/embeddings_cache.pkl` to free space

## Development

### Installing Development Dependencies
```bash
make install-dev
```

### Running Tests
```bash
make test
```

### Code Formatting
```bash
make format
```

### Code Linting
```bash
make lint
```

## Available Make Commands

```bash
make help          # Show all available commands
make setup         # Complete setup
make install       # Install production dependencies
make install-dev   # Install development dependencies
make run           # Generate a contract
make test-rag      # Test RAG retrieval
make test          # Run test suite
make logs          # Watch application logs
make clean         # Remove cache files
make clear-cache   # Clear embedding cache
make format        # Format code with black
make lint          # Lint code with flake8
```

## Architecture

### Retrieval-Augmented Generation (RAG)
1. **Load**: Contract templates from `data/contracts/`
2. **Embed**: Generate semantic embeddings (cached for speed)
3. **Retrieve**: Find most relevant templates for user request
4. **Generate**: Create contract using retrieved templates as context
5. **Review**: AI-powered legal review
6. **Revise**: Improve contract based on review

### Error Handling & Reliability
- Automatic API retries with exponential backoff
- Input validation on all user inputs
- Comprehensive error logging
- Graceful degradation when templates unavailable

### Performance
- **First run**: 10-30 seconds (embedding generation)
- **Subsequent runs**: 1-5 seconds (cached embeddings)
- **API calls**: 5-30 seconds per step

## License

[Your License Here]

## Support

For issues:
1. Check the logs: `tail logs/legal_ai_*.log`
2. Review the configuration: `cat .env`
3. Test retrieval: `make test-rag`
4. Check the README and documentation

## Contributing

1. Install development dependencies: `make install-dev`
2. Make your changes in `src/legal_ai/`
3. Add tests in `tests/`
4. Run tests: `make test`
5. Format code: `make format`
6. Commit and push

## Version History

### v1.0.0 (Current)
- Initial release
- RAG-based contract generation
- Gemini API integration
- Professional logging and error handling
- Comprehensive configuration
