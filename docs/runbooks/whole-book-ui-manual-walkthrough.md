# Whole-Book UI Manual Walkthrough

Short recurring product-truth check for the current whole-book reading surface.
This runbook exists because build output and omission accounting are not the
same thing as "can a real family reader move through the site, and does it feel
ready to ship?"

Companion history lane: `docs/ui-scout.md` and `docs/ui-scout/`

This lane is intentionally separate from `docs/scout/`, which is reserved for
external-source research.

## Canonical Surface

- Build the accepted bundle with `make build-family-site`
- Preview locally with `make preview-family-site`, or walk the exact public URL
  if the same shell is already deployed
- Keep the scenario centered on the current whole-book shell until repeated use
  proves that a second walkthrough is necessary

## What This Run Must Prove

- **Works**: the reading shell can carry a real person through the current
  whole-book landing page, representative chapters, family stories, and
  standalone pages without route hunting or confusing dead ends
- **Feels ready**: navigation is obvious, typography is legible, controls are
  large enough, and the site feels calm and trustworthy for older readers on
  desktop and mobile
- **Stays honest**: no important source material appears to disappear, and the
  public pages do not pretend deferred surfaces are already done

## Rules

- Use the surfaced reading site only
- Do not use `_internal/` maintenance artifacts unless they are needed to
  explain a defect
- Desktop and mobile are co-equal proof surfaces; do not mark a run `Pass`
  unless both pass
- Use `1280x900` as the default desktop viewport for recorded evidence
- Use `390x844` as the default mobile viewport for recorded evidence
- Every run must produce a dated report in `docs/ui-scout/` and update
  `docs/ui-scout.md`
- Every run must also update `docs/methodology/state.yaml` `ui_scout` so triage
  can see freshness truth
- If scripted screenshots are part of the evidence, wait for large page/image
  assets to finish painting before capture

## Exact Surfaced Path To Walk Today

1. Build the current site with `make build-family-site`
2. At desktop `1280x900`, start at `index.html`
   Pass if the grouped landing sections make it obvious where to go next
3. At desktop `1280x900`, open one representative non-family chapter such as
   `chapter-001.html`
   Pass if the reading page feels stable, legible, and easy to navigate
4. At desktop `1280x900`, open one representative family story such as
   `chapter-009.html`
   Pass if the family run still feels coherent inside the broader site
5. At desktop `1280x900`, open one standalone page or image entry such as
   `page-001.html`
   Pass if the entry is reachable and honestly presented
6. At desktop `1280x900`, use previous / contents / next navigation on at
   least one representative page
   Pass if the controls stay obvious, forgiving, and free of broken flow
7. Repeat the same surfaced path on mobile `390x844`:
   `index.html`, `chapter-001.html`, `chapter-009.html`, and `page-001.html`
8. On mobile `390x844`, use previous / contents / next navigation on at least
   one representative page
   Pass if the controls remain large, stacked cleanly, and stay easy to tap
9. Confirm both desktop and mobile remain free of horizontal overflow or hidden
   route-hunting traps across the checked path
10. Record the run in `docs/ui-scout/<date>-<surface>-<env>.md`, update
   `docs/ui-scout.md`, update `docs/methodology/state.yaml` `ui_scout`, and
   rerun `make methodology-compile`

## Pass / Fail Questions

- Could an older family member tell where to go next without explanation?
- Did any page feel cluttered, visually noisy, or hard to read?
- Did any navigation control feel too small, ambiguous, or easy to miss?
- Did any page imply that omitted or deferred material had vanished?
- Did desktop and mobile both independently pass the same core path?

## Record The Result

- Save screenshots or equivalent evidence for desktop landing, desktop
  representative reading pages, mobile landing, and mobile representative
  reading pages
- Write down the exact blocker or quality failure, including whether it is
  primarily functional, trust, polish, accessibility, or content
- Record the result in `docs/ui-scout/` and update `docs/ui-scout.md`
- If a product defect is discovered, create or link the focused follow-up story
  from the report instead of hiding it in the runbook
