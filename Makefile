.PHONY: clean build wheel dev install test lint format run all help

# Define Python interpreter to use
PYTHON = python
STREAMLIT = streamlit
PIP = pip
MODULE_NAME = agno_ai_multi_chat_app

all: clean build

# Build both wheel and sdist
build:
	$(PYTHON) -m build

# Build wheel only
wheel:
	$(PYTHON) -m build --wheel

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ .eggs/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -o -name "*.pyc" -exec rm -rf {} +

# Install in development mode
dev:
	$(PIP) install -e .

# Install the package from the wheel
install:
	$(PIP) install --force-reinstall dist/*.whl

# Run the main module
run:
	$(STREAMLIT) run $(MODULE_NAME)/launch_ui/app.py

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make build      - Build distribution packages"
	@echo "  make wheel      - Build wheel only"
	@echo "  make clean      - Remove all build/dist folders