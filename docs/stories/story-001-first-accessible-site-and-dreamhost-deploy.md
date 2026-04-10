---
title: "DreamHost Hosted Subdomain, DNS, and Static Deploy Path"
status: "Done"
priority: "High"
ideal_refs:
  - "1. Canonical Book Experience"
  - "5. Accessible Family Archive"
  - "6. Low-Friction Maintenance"
spec_refs:
  - "spec:5"
  - "spec:6"
  - "C5"
  - "C6"
  - "C7"
adr_refs: []
depends_on: []
category_refs:
  - "spec:5"
  - "spec:6"
  - "spec:7"
compromise_refs:
  - "C5"
  - "C6"
  - "C7"
input_coverage_refs: []
architecture_domains:
  - "site_experience"
roadmap_tags:
  - "bootstrap-canon-and-shell"
legacy_system: "DreamHost shared hosting plus Cloudflare public DNS"
---

# Story 001 — DreamHost Hosted Subdomain, DNS, and Static Deploy Path

**Priority**: High
**Status**: Done
**Decision Refs**: `docs/infrastructure.md`, `docs/RUNBOOK.md`, `README.md`, `docs/decisions/README.md`, DreamHost KB: `Proxy Server`, DreamHost KB: `Using a dreamhosters.com subdomain`, none found after search for repo-local ADRs
**Depends On**: None

## Goal

Establish the real hosting and DNS substrate for `onward.copper-dog.com` on
the existing DreamHost Shared Unlimited account, verify deploy access to the
hosted site directory, create a thin project-local deploy path for static site
uploads over SFTP, and record the operational truth in repo docs so later
site-shaping work can proceed locally without re-solving infrastructure.

## Acceptance Criteria

- [x] DreamHost hosting reality is verified, including plan type, shared server
      label, hosted subdomain path, and working deploy access.
- [x] Cloudflare public DNS for `onward.copper-dog.com` is configured to the
      DreamHost origin and the public hostname is freshly verified.
- [x] Repo truth surfaces record the hosting, DNS, and deploy-path facts needed
      for follow-on work.
- [x] A checked-in project-local `/deploy` skill exists for this repo's static
      DreamHost publish path and is backed by a repeatable local command.
- [x] One real deploy uploads the current staged static bundle from `input/` to
      DreamHost and is freshly verified over the public hostname.

## Out of Scope

- Crafting the final website presentation.
- Building the first local accessible content slice.
- NotebookLM podcast generation.
- ElevenLabs audiobook production.
- Any DreamHost plan upgrade or runtime beyond shared static hosting.

## Approach Evaluation

- **Simplification baseline**: The smallest honest move is to verify the
  existing shared-hosting and DNS path, then ship the current static export
  without inventing a heavier build/runtime layer.
- **AI-only**: Not sufficient. Browser-assisted account inspection helped, but
  terminal verification was still required for SFTP, DNS, and live hostname
  checks.
- **Hybrid**: Best fit. Use browser-visible hosting facts plus terminal
  verification and repo docs.
- **Pure code**: Appropriate only for the thin local deploy tool and its
  repeatable command surface.
- **Repo constraints / prior decisions**: No repo-local ADRs exist. DreamHost
  Shared Unlimited rules out proxy-backed app hosting and pushes the project
  toward a static-export-first site.
- **Existing patterns to reuse**: Methodology docs and generated story/index
  surfaces. Storybook's `/deploy` skill is a useful structural reference, but
  this repo should reduce it to static SFTP upload plus lightweight
  verification.
- **Eval**: The proof surface for this story is working SFTP access, a live
  Cloudflare-routed hostname, a checked-in deploy skill/command, and one real
  uploaded bundle verified publicly.

## Tasks

- [x] Verify the DreamHost hosting plan and shared-server details for the new
      hosted subdomain.
- [x] Verify the hosted site path and deploy access via SFTP.
- [x] Verify the Cloudflare DNS configuration and live public hostname for
      `onward.copper-dog.com`.
- [x] Inspect the current staged static bundle and select the exact directory
      to upload as the initial published site.
- [x] Inspect Storybook's `/deploy` skill and extract only the pieces that fit
      this repo's static SFTP deployment reality.
- [x] Create a project-local `/deploy` skill and its backing repeatable upload
      command for DreamHost static hosting.
- [x] Upload the current staged site bundle from `input/` to the DreamHost site
      path.
- [x] Freshly verify the deployed site over the public hostname with terminal
      checks and browser-style page inspection.
- [x] Record the hosting, DNS, and deploy-path truth in repo docs.
- [x] Store the DreamHost deploy credentials locally in a gitignored `.env`.
- [x] Run relevant checks for this story:
  - [x] `make methodology-compile`
  - [x] `make methodology-check`
  - [x] `dig +short onward.copper-dog.com`
  - [x] `curl -I http://onward.copper-dog.com`
  - [x] `curl -I https://onward.copper-dog.com`
  - [x] Verify SFTP login to the DreamHost shared server and inspect the remote
        site directory
  - [x] `scripts/sync-agent-skills.sh`
  - [x] `scripts/sync-agent-skills.sh --check`
  - [x] `make skills-check`
  - [x] Run the deploy command once against the staged static bundle
  - [x] Freshly inspect the public site content after upload
- [x] Search docs and update any that changed truth because of the chosen
      hosting and DNS path.
- [x] Verify project tenets:
  - [x] Honest operations: hosting and DNS truth is written down explicitly.
  - [x] Low-friction maintenance: later site work can reuse the recorded deploy
        substrate and local deploy skill.
  - [x] Accessibility substrate: public HTTPS hostname and deploy path exist for
        future accessible site slices.

## Workflow Gates

- [x] Build complete: infrastructure slice finished, required checks run, and
      summary shared
- [x] Validation complete or explicitly skipped by user
- [x] Story marked done via `/mark-story-done`

## Blocker Summary

N/A

## Blocker Evidence

N/A

## Unblock Condition

N/A

## Architectural Fit

- **Owning module / area**: Infrastructure truth, deploy path, public DNS
  routing, and the thin static deploy tool.
- **Methodology reality**: this story advances `spec:6` and reduces ambiguity
  around `spec:5`/`spec:7`, but still does not create the long-term site
  runtime itself.
- **Substrate evidence**: DreamHost Shared Unlimited account confirmed; shared
  server `iad1-shared-e1-33`; working SFTP login as `onward_user`; remote site
  path `/home/onward_user/onward.copper-dog.com`; Cloudflare `A` record for
  `onward` pointing at DreamHost origin `208.113.159.28`; public hostname
  verified via `curl`.
- **Data contracts / schemas**: No canonical content contract was introduced in
  this story.
- **File sizes**: `README.md` (46), `docs/RUNBOOK.md` (22),
  `docs/infrastructure.md` (75).
- **Decision context**: Reviewed `AGENTS.md`, `README.md`, `docs/ideal.md`,
  `docs/spec.md`, `docs/RUNBOOK.md`, `docs/infrastructure.md`,
  `docs/methodology/state.yaml`, `docs/methodology/graph.json`, and DreamHost
  KB docs. No repo-local ADRs exist.

## Files to Modify

- `.env` — local gitignored DreamHost deploy credentials, site path, and local
  default source bundle path
- `.gitignore` — ignore local `.env`
- `Makefile` — expose the deploy command as `make deploy-static`
- `requirements-deploy.txt` — pinned Python dependency for the deploy helper
- `README.md` — record confirmed hosting/DNS truth
- `docs/RUNBOOK.md` — point to infrastructure truth
- `docs/infrastructure.md` — canonical hosting/DNS/deploy surface
- `.agents/skills/deploy/SKILL.md` — project-local static DreamHost deploy
  skill
- `scripts/deploy_static_site.py` — repeatable SFTP upload command

## Redundancy / Removal Targets

- Stale assumptions that `doc-web` integration was the active hosting concern.
- Future private deploy notes that duplicate `docs/infrastructure.md`.

## Notes

- The actual website shaping belongs in a separate follow-up story.
- Shared hosting plus Cloudflare makes a static-export-first site the default
  until evidence justifies something heavier.

## Plan

1. Reopen the story around a thin static deploy requirement rather than only
   passive infrastructure facts.
2. Implement a project-local `/deploy` skill backed by a repeatable Python
   upload command that reads local `.env` values, uploads the current staged
   static bundle over SFTP, and emits enough evidence to inspect what landed.
3. Use the existing `input/doc-web-html/story206-onward-proof-r10` bundle as
   the first deployed payload, then verify the public hostname with terminal
   checks and browser-style page inspection.
4. Update infrastructure/runbook/readme truth surfaces to point at the real
   deploy command and live initial bundle.

## Work Log

20260410-1243 — action: created story from inbox items 4 and 5, result:
captured the site/runtime/deploy line as the primary work package, evidence:
`docs/inbox.md` and current repo state, next step: inspect `input/` and
DreamHost constraints to make the story build-ready.
20260410-1243 — action: build-story exploration, result: verified the staged
source snapshot exists at
`/Users/cam/Documents/Projects/onward-to-the-unknown-website/input` with a
manifest-backed HTML export (`story206-onward-proof-r10`) containing 24
chapters, 9 page entries, images, and provenance JSONL; confirmed there is
still no runtime in the repo; checked DNS and found no public
`onward.copper-dog.com` record while `copper-dog.com` delegates to Cloudflare;
reviewed current DreamHost hosting docs and found proxy-backed Node/Python apps
require Managed VPS or Dedicated, evidence: local `manifest.json`, `dig`
results from 2026-04-10, DreamHost KB pages on proxy hosting and
`dreamhosters.com` subdomains, next step: confirm the actual hosting plan,
panel access path, and DNS control path before treating the story as buildable.
20260410-1243 — action: infrastructure truth update, result: recorded the
confirmed DreamHost `Shared Unlimited` plan in `docs/infrastructure.md` from a
user-provided screenshot and updated the blocker to focus on shared-hosting
publish path plus DNS control rather than unknown hosting class, evidence:
DreamHost account screenshot in this thread and updated infrastructure doc,
next step: inspect the site entry inside DreamHost and the DNS zone details to
identify the exact publish path for `onward.copper-dog.com`.
20260410-1243 — action: hosting-path refinement, result: recorded that
`copper-dog.com` is already a hosted DreamHost site on `iad1-shared-e1-33` and
that sibling `copper-dog.com` subdomains already exist on the same shared plan,
evidence: user-provided DreamHost Websites screenshot in this thread, next
step: inspect the Add Website or Manage flow for `onward.copper-dog.com` to
capture the directory/user and then map the required Cloudflare DNS record.
20260410-1243 — action: deploy-access verification, result: saved the DreamHost
credentials in a local gitignored `.env`, verified SFTP login to
`iad1-shared-e1-33.dreamhost.com` as `onward_user`, confirmed the remote site
path `/home/onward_user/onward.copper-dog.com`, and observed the default
starter files in that directory, evidence: current-pass SFTP session, next
step: confirm the Cloudflare DNS destination and then start the static site
implementation and upload path.
20260410-1250 — action: blocker reassessment, result: the user supplied a final
DreamHost/Cloudflare setup report confirming the Cloudflare `A` record for
`onward.copper-dog.com` points at DreamHost origin IP `208.113.159.28` with
proxying enabled; terminal verification now shows the hostname resolves to
Cloudflare edge IPs and returns `HTTP 200` over both HTTP and HTTPS, evidence:
user-provided report plus `dig +short onward.copper-dog.com`,
`curl -I http://onward.copper-dog.com`, and
`curl -I https://onward.copper-dog.com`, next step: treat the story as
buildable, use a static-export-first implementation path, and stop at the human
plan gate before writing site code.
20260410-1258 — action: rescope-and-close, result: narrowed Story 001 to the
actually shipped infrastructure slice, moved remaining website-shaping work into
Story 004, and closed this story on the basis of live hosting/DNS/SFTP evidence
plus repo doc updates, evidence: `docs/infrastructure.md`, live hostname
checks, SFTP session, and regenerated story index, next step: `/check-in-diff`.
20260410-1307 — action: close-out validation sweep, result: reran
`make methodology-compile` and `make methodology-check` successfully after the
rescope; also ran `python -m pytest tests/` and
`python -m ruff check modules/ tests/`, which are not currently meaningful
project gates because the repo has no collected tests and no `modules/`
directory, evidence: current-pass command output on 2026-04-10, next step:
`/check-in-diff`.
20260410-1418 — action: story reopened, result: moved the thin static deploy
skill and first real upload back into Story 001 after user direction, evidence:
user instruction in this thread plus absence of any existing deploy skill in
`.agents/skills/`, next step: implement the minimal DreamHost SFTP deploy
command and verify a live upload from `input/`.
20260410-1421 — action: deploy-tool exploration, result: confirmed the staged
bundle to publish is
`/Users/cam/Documents/Projects/onward-to-the-unknown-website/input/doc-web-html/story206-onward-proof-r10`
and that Storybook's deploy skill is Fly-oriented rather than reusable as-is,
evidence: local `manifest.json`, `index.html`, and
`/Users/cam/Documents/Projects/Storybook/storybook/.agents/skills/deploy/SKILL.md`,
next step: implement a thin DreamHost SFTP upload command instead of adapting
Fly-specific release logic.
20260410-1428 — action: deploy-tool implementation, result: added
`scripts/deploy_static_site.py`, a repo-local `/deploy` skill, `make deploy-static`,
and runbook/readme/infrastructure updates; synced skill wrappers and verified
`make skills-check`, evidence: current-pass file edits plus
`./scripts/sync-agent-skills.sh`, `./scripts/sync-agent-skills.sh --check`,
and `make skills-check`, next step: run one real upload against DreamHost.
20260410-1436 — action: live static deploy, result: uploaded the contents of
`story206-onward-proof-r10` to `/home/onward_user/onward.copper-dog.com` over
SFTP and verified `index.html`, `chapter-001.html`, `images/`, and
`provenance/` exist remotely, evidence: current-pass `python scripts/deploy_static_site.py`
transcript, next step: verify the public hostname and rendered content.
20260410-1438 — action: public verification, result: verified
`https://onward.copper-dog.com/`, `chapter-001.html`,
`images/page-001-000.jpg`, and `provenance/blocks.jsonl` return `HTTP 200`,
and confirmed homepage/chapter content via browser-style public page
inspection, evidence: current-pass `curl` output, `dig +short`, and public page
inspection of `https://onward.copper-dog.com/` and
`https://onward.copper-dog.com/chapter-001.html`, next step: `/validate` or
`/mark-story-done`.
20260410-1534 — action: repeatability hardening, result: replaced blind upload
behavior with a manifest-backed SFTP sync, added `requirements-deploy.txt` for
the pinned `pexpect` dependency, and proved stale-file removal by deploying a
temporary bundle containing `deploy-probe.txt` and then redeploying the
canonical bundle until `deploy-probe.txt` returned `HTTP 404`, evidence:
current-pass deploy transcripts, `curl -I https://onward.copper-dog.com/deploy-probe.txt`,
and equality checks between local and public `index.html`,
`chapter-001.html`, and `provenance/blocks.jsonl`, next step: `/validate` or
`/mark-story-done`.
20260410-1547 — action: close-out gate fix, result: added focused tests for the
deploy sync planner and a minimal `modules/` package so the repo-level
`/mark-story-done` Python checks can run cleanly, evidence:
`tests/test_deploy_static_site.py` and `modules/__init__.py`, next step:
rerun close-out validation and mark the story done.
20260410-1603 — action: mark-story-done close-out, result: reran the required
Python validation gates successfully (`python -m pytest tests/`,
`python -m ruff check modules/ tests/`) after fixing the stale-path assertion
order in `tests/test_deploy_static_site.py`, confirmed the story still has full
acceptance-criteria coverage and no open blockers, and marked Story 001 done,
evidence: current-pass validation output on 2026-04-10 and this updated story
record, next step: `/check-in-diff`.
