.PHONY: init install snapshot help

help:
	@echo "DAF commands:"
	@echo "  make init      One-shot template setup (run once after cloning)"
	@echo "  make install   Install/sync deps via uv"
	@echo "  make snapshot  Generate docs/data_dictionary.md from data files"

init:
	python3 scripts/init_project.py

install:
	uv sync

snapshot:
	uv run python scripts/snapshot.py
