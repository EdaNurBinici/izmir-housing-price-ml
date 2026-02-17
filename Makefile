.PHONY: help install install-dev train run test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make train        - Train the model"
	@echo "  make run          - Run the Streamlit application"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Format code (black + isort)"
	@echo "  make clean        - Remove generated files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

train:
	python model_egitim.py

run:
	streamlit run app.py

test:
	pytest tests/ -v

lint:
	ruff check .
	black --check .
	isort --check-only .

format:
	black .
	isort .
	ruff check . --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf logs/*.log
