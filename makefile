# Makefile for a Python project

# Variables
PYTHON = python3
VENV = venv
REQUIREMENTS = requirements.txt
APP = app.py

# Default target
all: help

# Help command
help:
	@echo "Makefile commands:"
	@echo "  make venv       Create a virtual environment"
	@echo "  make install    Install dependencies"
	@echo "  make run        Run the application"
	@echo "  make test       Run all tests"
	@echo "  make clean      Remove __pycache__ and other temp files"

# Create a virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	@. $(VENV)/bin/activate; pip install -r $(REQUIREMENTS)

# Run the application
run:
	@echo "Running the application..."
	@. $(VENV)/bin/activate; $(PYTHON) $(APP)

# Run all tests
test:
	@echo "Running functional tests..."
	@. $(VENV)/bin/activate; pytest functionaltest_app.py
	@echo "Running integration tests..."
	@. $(VENV)/bin/activate; pytest integrationtest_app.py
	@echo "Running performance tests..."
	@. $(VENV)/bin/activate; pytest performancetest_app.py
	@echo "Running security tests..."
	@. $(VENV)/bin/activate; pytest securitytest_app.py
	@echo "Running unit tests..."
	@. $(VENV)/bin/activate; pytest unittest_app.py

# Clean up temporary files
clean:
	@echo "Cleaning up temporary files..."
	rm -rf __pycache__/
	rm -rf $(VENV)
	rm -rf *.egg-info
