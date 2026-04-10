PYTHON ?= $(shell command -v python 2>/dev/null || command -v python3 2>/dev/null)
FAMILY_SITE_OUTPUT ?= build/family-site
FAMILY_SITE_PORT ?= 4173

.PHONY: skills-sync skills-check methodology-compile methodology-check deploy-static test lint build-family-site preview-family-site refresh-omission-audit doc-web-contract doc-web-run-onward doc-web-import-run doc-web-import-bundle

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

test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m ruff check modules/ scripts/ tests/

build-family-site:
	$(PYTHON) scripts/build_family_site.py \
		$(if $(SOURCE),--source "$(SOURCE)",) \
		--output "$(FAMILY_SITE_OUTPUT)"

preview-family-site:
	$(PYTHON) -m http.server "$(FAMILY_SITE_PORT)" --directory "$(FAMILY_SITE_OUTPUT)"

refresh-omission-audit: build-family-site
	cp "$(FAMILY_SITE_OUTPUT)/_internal/omission-audit.json" docs/omission-audit.json

doc-web-contract:
	$(PYTHON) scripts/doc_web_import.py contract

doc-web-run-onward:
	$(PYTHON) scripts/doc_web_import.py run-onward

doc-web-import-run:
	$(PYTHON) scripts/doc_web_import.py import-run

doc-web-import-bundle:
	$(PYTHON) scripts/doc_web_import.py import-bundle
