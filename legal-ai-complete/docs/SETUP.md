# Setup Guide for Legal AI Contract Generator

## System Requirements

- **Python**: 3.8 or higher
- **pip**: Package installer
- **virtualenv** (recommended): For isolated environments
- **Git**: For version control

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd legal-ai

# Or if downloaded as zip
unzip legal-ai.zip
cd legal-ai
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Option 1: Using make (recommended)
make setup

# Option 2: Manual installation
pip install -r requirements.txt
mkdir -p data/contracts data/embeddings data/outputs logs
```

### 4. Configure Environment

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

#### Required Configuration
You **must** set your Gemini API key:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or get your API key
3. Add it to `.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

#### Optional Configuration
Other settings have sensible defaults, but you can customize:

```env
# Model selection
GEMINI_MODEL=gemini-2.5-pro

# Generation parameters (0.0-1.0, lower = more deterministic)
TEMPERATURE=0.2

# Maximum response length
MAX_OUTPUT_TOKENS=8192

# Number of contract templates to retrieve
RETRIEVAL_TOP_K=2

# Split large contracts into chunks (words per chunk)
CHUNK_SIZE=500

# Jurisdiction for contracts
JURISDICTION=England and Wales

# Enable detailed logging
DEBUG=true
```

### 5. Add Contract Templates (Optional)

Place your contract template files in `data/contracts/`:

```bash
# Example with sample contracts
cp my_contracts/*.txt data/contracts/

# Or create a sample
echo "Sample NDA content..." > data/contracts/nda_template.txt
```

The system will work without templates (generates from scratch) but performs better with examples.

## Verification

### Test Installation

```bash
# Quick test to ensure everything works
make test-rag
```

Expected output:
```
Testing RAG with 0 documents

Query: 'confidentiality obligations'
------------------------------------------------------------
No results found
```

(No documents is fine - just verifies the system loads)

### Run Full Application

```bash
# Generate a contract
make run
```

You'll be prompted:
```
====================================
 AI LEGAL CONTRACT GENERATOR
====================================

Describe the contract you want:

>
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'google'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "API key error" or "authentication failed"

**Solution**: Check your .env file
```bash
# Verify the key is set
cat .env | grep GEMINI_API_KEY

# Make sure it's not a placeholder
# Wrong: GEMINI_API_KEY=your_key_here
# Right: GEMINI_API_KEY=AIzaSyD...
```

### "No contracts found"

**Solution**: This is normal! Add contract templates:
```bash
cp your_contracts/*.txt data/contracts/
```

Or test with a sample:
```bash
echo "This is a sample contract..." > data/contracts/sample.txt
make test-rag
```

### "Out of memory"

**Solution**: Reduce chunk size in `.env`:
```env
CHUNK_SIZE=250  # Smaller chunks
```

Or clear the cache:
```bash
make clear-cache
```

### "Cannot find contracts directory"

**Solution**: Create it manually
```bash
mkdir -p data/contracts data/embeddings data/outputs logs
```

## Development Setup

For development, also install dev dependencies:

```bash
# Install development tools
make install-dev

# Or manually
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=src

# Run specific test
pytest tests/test_rag.py -v
```

### Code Quality

```bash
# Format code
make format

# Check style
make lint

# Both
make format lint
```

## Docker Setup (Optional)

If you prefer Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "src.legal_ai.main"]
```

Build and run:
```bash
docker build -t legal-ai .
docker run -e GEMINI_API_KEY=your_key -v $(pwd)/data:/app/data legal-ai
```

## Next Steps

1. ✅ Installed dependencies
2. ✅ Configured API key
3. ✅ Verified installation
4. Next: Add contract templates
5. Next: Generate your first contract!

## Getting Help

1. Check the **README.md** for overview
2. Review **logs/legal_ai_*.log** for errors
3. Run **make help** for available commands
4. Test with **make test-rag**

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Delete project folder
rm -rf legal-ai

# Or just remove virtual environment
rm -rf legal-ai/venv
```
