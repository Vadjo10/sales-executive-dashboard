.PHONY: help install dev lint format test typecheck clean run

help:
	@echo "Commands:"
	@echo "  make install    - Install production dependencies"
	@echo "  make dev        - Install dev dependencies"
	@echo "  make lint       - Run flake8"
	@echo "  make format     - Run black and isort"
	@echo "  make test       - Run pytest with coverage"
	@echo "  make typecheck  - Run mypy"
	@echo "  make clean      - Remove cache files"
	@echo "  make run        - Run pipeline"

install:
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt

lint:
	flake8 src/ tests/

format:
	black src/ tests/
	isort src/ tests/

test:
	pytest --cov=src/ --cov-report=term-missing --cov-report=html

typecheck:
	mypy src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

run:
	python -m scripts.run_pipeline
