PYTHON ?= $(shell command -v python 2>/dev/null || command -v python3 2>/dev/null)
FAMILY_SITE_OUTPUT ?= build/family-site
FAMILY_SITE_PORT ?= 4173
AUDIOBOOK_SCRIPT_OUTPUT ?= audiobook/script
FULL_AUDIOBOOK_MANIFEST ?= audiobook/manifest.json
PORTABLE_MANIFEST ?= portable/manifest.json
EPUBCHECK_JAR ?= .runtime/epubcheck-5.3.0/epubcheck.jar

.PHONY: skills-sync skills-check methodology-compile methodology-check deploy-static test lint test-portable-editions test-reunion-flyer build-family-site build-audiobook-script build-full-audiobook build-epub build-m4b build-portable-editions validate-portable-editions validate-public-portable build-reunion-flyer validate-reunion-flyer reunion-flyer preview-family-site refresh-omission-audit doc-web-contract doc-web-run-onward doc-web-import-run doc-web-import-bundle

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

test-portable-editions:
	$(PYTHON) -m pytest tests/test_portable_editions.py tests/test_build_m4b.py

test-reunion-flyer:
	$(PYTHON) -m pytest tests/test_reunion_flyer.py

build-family-site:
	$(PYTHON) scripts/build_family_site.py \
		$(if $(SOURCE),--source "$(SOURCE)",) \
		$(if $(RELEASE),--release,) \
		--output "$(FAMILY_SITE_OUTPUT)"

build-audiobook-script:
	$(PYTHON) scripts/build_audiobook_script.py \
		$(if $(SOURCE),--source "$(SOURCE)",) \
		$(if $(FORCE),--force,) \
		--output "$(AUDIOBOOK_SCRIPT_OUTPUT)"

build-full-audiobook:
	$(PYTHON) scripts/build_full_audiobook.py \
		--manifest "$(FULL_AUDIOBOOK_MANIFEST)" \
		$(if $(OUTPUT),--output "$(OUTPUT)",) \
		$(if $(FORCE),--force,)

build-epub:
	$(PYTHON) scripts/portable_editions.py build-epub \
		--manifest "$(PORTABLE_MANIFEST)" \
		$(if $(FORCE),--force,)

build-m4b:
	$(PYTHON) scripts/build_m4b.py build \
		--portable-manifest "$(PORTABLE_MANIFEST)" \
		--audiobook-manifest "$(FULL_AUDIOBOOK_MANIFEST)" \
		$(if $(FORCE),--force,)

build-portable-editions: build-epub build-m4b
	$(MAKE) build-family-site RELEASE=1

validate-portable-editions:
	$(PYTHON) scripts/portable_editions.py validate-epub \
		--manifest "$(PORTABLE_MANIFEST)" \
		--epubcheck \
		--epubcheck-jar "$(EPUBCHECK_JAR)"
	$(PYTHON) scripts/build_m4b.py validate \
		--portable-manifest "$(PORTABLE_MANIFEST)" \
		--audiobook-manifest "$(FULL_AUDIOBOOK_MANIFEST)"

validate-public-portable:
	$(PYTHON) scripts/portable_editions.py validate-public \
		--manifest "$(PORTABLE_MANIFEST)" \
		$(if $(BASE_URL),--base-url "$(BASE_URL)",)

build-reunion-flyer:
	$(PYTHON) scripts/reunion_flyer.py build

validate-reunion-flyer:
	$(PYTHON) scripts/reunion_flyer.py validate

reunion-flyer: test-reunion-flyer build-reunion-flyer validate-reunion-flyer

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
