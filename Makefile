.PHONY: help setup install install-dev run test test-rag logs clean clear-cache format lint

help:
	@echo ""
	@echo "Legal AI Contract Generator"
	@echo "---------------------------"
	@echo "make setup        Complete first-time setup"
	@echo "make install      Install production dependencies"
	@echo "make install-dev  Install development dependencies"
	@echo "make run          Generate a contract"
	@echo "make test-rag     Test the retrieval system"
	@echo "make test         Run the full test suite"
	@echo "make logs         Tail application logs"
	@echo "make clean        Remove .pyc files and __pycache__"
	@echo "make clear-cache  Delete cached embeddings"
	@echo "make format       Format code with black"
	@echo "make lint         Lint code with flake8"
	@echo ""

setup: install
	mkdir -p data/contracts data/embeddings data/outputs logs
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example — add your GEMINI_API_KEY"; fi

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python -m src.legal_ai.main

test-rag:
	python tests/test_rag.py

test:
	pytest tests/ -v

logs:
	tail -f logs/legal_ai_*.log

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage

clear-cache:
	rm -f data/embeddings/embeddings_cache.pkl
	@echo "Embedding cache cleared."

format:
	black src/ tests/

lint:
	flake8 src/ tests/ --max-line-length=100
