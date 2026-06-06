.PHONY: install run debug clean lint lint-strict

PYTHON = python3
CONFIG = config.txt
MAIN_SCRIPT = a_maze_ing.py

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache dist/ build/ mazegen_amazeing.egg-info/
	rm -f maze.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
