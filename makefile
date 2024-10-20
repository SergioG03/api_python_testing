# Variables
PYTHON = python3
VENV = venv
REQUIREMENTS = requirements.txt
APP = app.py
COVERAGE_REQS = coverage.txt
TRIVY_REQS = trivy.txt

# Default target
all: help

# Help command
help:
	@echo "Makefile commands:"
	@echo "  make venv       Create a virtual environment"
	@echo "  make install    Install dependencies"
	@echo "  make run        Run the application"
	@echo "  make test       Run all tests"
	@echo "  make coverage   Run coverage analysis"
	@echo "  make trivy      Run trivy vulnerability scan"
	@echo "  make clean      Remove __pycache__ and other temp files"

# Create a virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	@. $(VENV)/bin/activate; pip install -r $(REQUIREMENTS)
	@echo "Installing coverage and trivy..."
	@. $(VENV)/bin/activate; pip install -r $(COVERAGE_REQS)
	@. $(VENV)/bin/activate; pip install -r $(TRIVY_REQS)

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

# Run coverage analysis
coverage: install
	@echo "Running coverage analysis..."
	@. $(VENV)/bin/activate; coverage run --source=$(APP) -m pytest
	@. $(VENV)/bin/activate; coverage report -m

# Run trivy vulnerability scan
trivy: install
	@echo "Running trivy vulnerability scan..."
	@. $(VENV)/bin/activate; trivy image $(VENV)

# Clean up temporary files
clean:
	@echo "Cleaning up temporary files..."
	rm -rf __pycache__/
	rm -rf $(VENV)
	rm -rf *.egg-info
	rm -rf.coverage

