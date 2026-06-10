.PHONY: help install install-dev run test clean logs setup clear-cache format lint test-rag

help:
	@echo "Legal AI Contract Generator - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Complete setup (install, create dirs)"
	@echo "  make install      - Install dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run          - Generate a contract"
	@echo "  make test-rag     - Test RAG retrieval"
	@echo ""
	@echo "Development:"
	@echo "  make test         - Run test suite"
	@echo "  make logs         - Watch application logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Remove cache and compiled files"
	@echo "  make clear-cache  - Remove embedding cache"

setup: install
	@echo "Creating data directories..."
	@mkdir -p data/contracts data/embeddings data/outputs
	@mkdir -p logs
	@echo "Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Copy .env.example to .env and set GEMINI_API_KEY"
	@echo "  2. Add .txt contract files to data/contracts/"
	@echo "  3. Run: make run"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	python -m src.legal_ai.main

test-rag:
	python -m tests.test_rag

test:
	pytest tests/ -v --cov=src

logs:
	tail -f logs/legal_ai_*.log

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

clear-cache:
	rm -f data/embeddings/embeddings_cache.pkl
	@echo "Embedding cache cleared"

format:
	black src/ tests/

lint:
	flake8 src/ tests/

.DEFAULT_GOAL := help
