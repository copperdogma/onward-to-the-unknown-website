PYTHON ?= $(shell command -v python 2>/dev/null || command -v python3 2>/dev/null)

.PHONY: skills-sync skills-check methodology-compile methodology-check deploy-static

skills-sync:
	./scripts/sync-agent-skills.sh

skills-check:
	./scripts/sync-agent-skills.sh --check

methodology-compile:
	$(PYTHON) scripts/methodology_graph.py build

methodology-check:
	$(PYTHON) scripts/methodology_graph.py check

deploy-static:
	$(PYTHON) scripts/deploy_static_site.py
