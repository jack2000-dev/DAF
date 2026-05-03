.PHONY: install snapshot help

help:
	@echo "DAF commands:"
	@echo "  make install   Install/sync deps via uv"
	@echo "  make snapshot  Generate docs/data_dictionary.md from data files"

install:
	uv sync

snapshot:
	uv run python scripts/snapshot.py
