.DEFAULT_GOAL := install

PYTHON_VERSION := python3.12

.PHONY: install
install:
	python -m pip install -U pip
	pip install -r ./backend/requirements.txt

.PHONY: run
run:
	python -m uvicorn main:create_app --reload --factory --port 5002
