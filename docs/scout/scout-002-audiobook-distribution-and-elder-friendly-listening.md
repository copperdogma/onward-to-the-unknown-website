# Scout 002 - audiobook-distribution-and-elder-friendly-listening

**Source:** Local repo audiobook surface plus current official vendor docs
**Scouted:** 2026-04-12
**Scope:** Compare the shipped on-site audiobook flow against current free or
effectively no-cost off-site lanes for a family-first listening experience
**Previous:** None
**Status:** Done

## Decision

- **Recommended first publishing lane:** keep the audiobook canonical on
  `onward.copper-dog.com` through the existing site-hosted MP3 flow.
- **Recommended first website listening pattern:** lead with
  `Play Full Audiobook`, `Download Full Audiobook`, and page-level
  `Listen to this section` actions, with explicit copy that says no app or
  account is required.
- **Recommended first off-site duplicate, if one is later needed:** Spotify
  direct upload, but only as a secondary convenience lane after the site-first
  family flow is live and accepted.

## Local Baseline

The repo already has the critical on-site substrate:

- `audiobook/manifest.json` is the canonical track inventory for the reviewed
  MP3 set.
- `make build-family-site` emits `build/family-site/audiobook.html`, publishes
  the referenced `audiobook/` MP3 files, and adds page-level listening panels
  to matching chapters and supplements.
- `scripts/deploy_static_site.py` already publishes `audiobook.html` and
  generated `audiobook/` assets to the DreamHost-hosted site bundle.

This means the project does not need a third-party platform to satisfy the
current family goal of "press play or download without confusion."

## Lane Comparison

| Lane | Uses current reviewed MP3 audiobook? | Listener friction | Operator overhead | Fit for this family-first goal |
|---|---|---|---|---|
| Current site-hosted MP3 flow | Yes | Lowest: browser play and direct download, no extra account | Lowest: already wired into build and deploy | **Best first lane** |
| ElevenReader Publishing | No; it distributes text and generates narration on demand | Medium to high: share link/QR flow, app/web ambiguity, no MP3 download | Medium: manuscript upload, review, payouts, product-specific limits | Not a primary audiobook lane |
| Spotify for Authors direct upload | Yes | Medium to high: purchase or subscription context plus Spotify account/app expectations | Medium: metadata, payment profile, cover art, sample, pricing | Best secondary off-site lane, not first |
| Voices by INaudio | Yes, through LPF ingest | High: retail/library distribution, delayed availability, storefront context | High: ISBN, pricing, royalties, retailer setup | Too commerce-oriented for the first family lane |
| Audio Native | Not as a distribution shelf; it is an embedded player on your own site | Medium: depends on webpage embed, not a discovery lane | Medium: Creator-plan-or-higher dependency plus embed work | Solves the wrong problem |
| ElevenLabs Video | No | High | High | Out of scope; not an audiobook lane |

## Findings

1. **The current website is already the only lane that preserves all four priorities at once** - HIGH value
   The on-site flow is the only researched option that is simultaneously
   no-charge to listeners, free of app/account setup, built around the existing
   reviewed MP3 files, and immediate to ship from current repo infrastructure.
   For older relatives, that combination matters more than marketplace reach.

2. **ElevenReader is attractive on cost but wrong for the artifact this repo already owns** - HIGH value
   ElevenReader Publishing is free and accepts manuscript formats such as EPUB,
   PDF, TXT, DOCX, and HTML, but it does not accept external audio uploads.
   The audio is generated on demand inside ElevenReader, users choose voices
   themselves, and the generated content is intended for in-app streaming
   rather than export. That makes it a text-to-speech reading lane, not a way
   to distribute the repo's existing reviewed MP3 audiobook.

3. **Spotify direct upload is the cleanest external duplicate lane, but it is still not the family-default experience** - HIGH value
   Spotify for Authors is free to upload, non-exclusive, keeps ownership with
   the author, and explicitly accepts digital voice narration from ElevenLabs.
   It also gives listeners one-time unlock purchases, app playback, and
   offline download. But that still introduces purchase flow, Spotify account
   assumptions, and store/app expectations that the current family goal is
   trying to avoid.

4. **Voices by INaudio is a real distribution network, but it is built for commercial retail/library rollout rather than simple family access** - MEDIUM value
   INaudio accepts already-created audiobooks, including AI-narrated LPF files
   from ElevenLabs, keeps rights with the author, can auto-assign an ISBN, and
   pushes to other retailers. It also requires pricing, royalty/payment setup,
   and a waiting period before titles go live. That is useful only if broad
   retail presence becomes a deliberate goal later.

5. **Audio Native and ElevenLabs Video should be rejected for this story** - MEDIUM value
   Audio Native is an on-site embed product available on Creator plan and above;
   it can voice webpage text or embed Studio output, but it does not solve the
   family discovery/distribution problem that the site-hosted MP3 lane already
   solves more simply. ElevenLabs Video is not an audiobook lane at all.

6. **Spotify's own market-count docs currently drift, which is another reason not to make it the family's primary access path** - LOW value
   The current availability article lists audiobook listening markets including
   the United States and Canada, while the referral-partner article still says
   direct-upload audiobooks are available in 14 countries. The exact count does
   not change this story's recommendation, but it is a reminder that external
   platform rules and messaging move faster than the repo's preferred launch
   path.

## Recommendation

### First Publishing Lane

Use the current site itself as the first published audiobook lane:

- deploy `audiobook.html`
- deploy the reviewed chapter MP3s
- deploy the merged full-audiobook MP3 when it exists
- keep the website as the canonical home for family listening

This aligns with the Ideal by preserving provenance, reducing friction for
older readers, and avoiding a paid-storefront default.

### First Website Listening Pattern

The reader-facing pattern should stay extremely plain:

- homepage and audiobook panel:
  `Play Full Audiobook` and `Download Full Audiobook`
- audiobook page:
  full-book play/download first, then clear chapter cards
- chapter/supplement pages:
  `Listen to this section`
- explanatory copy:
  `No app or account needed. Press play here, or download an MP3 to keep on your phone, tablet, or computer.`

The key rule is that a relative should be able to start listening from the
website itself before being asked to install anything, create an account, or
understand store logic.

### Secondary Off-Site Lane

If the project later wants one external duplicate, use Spotify direct upload
first, but keep it secondary:

- it preserves the existing narrated audio files
- it is free to upload and non-exclusive
- it supports digital voice narration from ElevenLabs
- it still adds purchase/account/app friction, so it should never replace the
  site-hosted family path

## Required Assets And Metadata By Lane

### Site-hosted first lane

- existing reviewed MP3 files
- `audiobook/manifest.json`
- homepage/audiobook/chapter copy that says play/download is available without
  an app or account

### Spotify secondary lane

- uploaded audio files in MP3, WAV, or FLAC
- square cover art in PNG or JPEG
- audiobook details and metadata
- chapter names
- sample file
- payment profile
- explicit digital-voice disclosure enabled at upload time

### Voices by INaudio secondary lane

- LPF package exported from ElevenLabs
- metadata and cover art
- retail/library pricing
- ISBN decision or platform-assigned ISBN
- royalty payout setup
- retailer selection

### ElevenReader experiment lane

- source manuscript in EPUB, PDF, TXT, DOCX, or HTML
- acceptance that the platform will generate narration on demand instead of
  using the repo-owned MP3 audiobook
- acceptance that listeners will not get the same direct-download MP3 workflow

## Open Questions

- Does the project want any external app/store duplicate at all, or is the
  family website itself sufficient?
- If Spotify later becomes a secondary lane, what cover image, description,
  sample clip, and price should be used?
- Before any retail launch, do the current voice/model choices and any
  provider-specific output terms permit the exact external distribution the
  project wants? This scout did not reinterpret contract language.

## Verification

- `make methodology-compile`
- `make methodology-check`
- manual review of this scout for plain-language clarity and older-reader fit

## Evidence

- Local repo evidence reviewed:
  - `docs/infrastructure.md`
  - `docs/RUNBOOK.md`
  - `docs/presentation-decisions.md`
  - `docs/runbooks/elevenlabs-audiobook.md`
  - `audiobook/manifest.json`
  - `modules/build_family_site.py`
- Official sources reviewed on 2026-04-12:
  - ElevenLabs: [Are there any costs associated with ElevenReader Publishing?](https://help.elevenlabs.io/hc/en-us/articles/32443819372945-Are-there-any-costs-associated-with-ElevenReader-Publishing)
  - ElevenLabs: [What formats are supported for publication?](https://help.elevenlabs.io/hc/en-us/articles/32062739207185-What-formats-are-supported-for-publication)
  - ElevenLabs: [Can I provide my own audio files for narration?](https://help.elevenlabs.io/hc/en-us/articles/32443936656145-Can-I-provide-my-own-audio-files-for-narration)
  - ElevenLabs: [How can I share my book with my audience?](https://help.elevenlabs.io/hc/en-us/articles/32444327177489-How-can-I-share-my-book-with-my-audience)
  - ElevenLabs: [Is ElevenReader available for Desktop or Web?](https://help.elevenlabs.io/hc/en-us/articles/38319697008657-Is-ElevenReader-available-for-Desktop-or-Web)
  - ElevenLabs: [Can I use content generated in ElevenReader for commercial use?](https://help.elevenlabs.io/hc/en-us/articles/26666038808209-Can-I-use-content-generated-in-ElevenReader-for-commercial-use)
  - ElevenLabs: [What is Audio Native?](https://help.elevenlabs.io/hc/en-us/articles/26970150960401-What-is-Audio-Native)
  - Spotify: [Uploading audiobooks to Spotify for Authors](https://support.spotify.com/by-en/authors/article/uploading-audiobooks/)
  - Spotify: [Digital voice narration](https://support.spotify.com/lb-en/authors/article/digital-voice-narration/)
  - Spotify: [Where are audiobooks available on Spotify?](https://support.spotify.com/us/authors/article/audiobooks-availability/)
  - Spotify: [Getting your audiobook on other listening platforms](https://support.spotify.com/sg-en/authors/article/getting-your-audiobook-on-other-listening-platforms/)
  - Spotify: [Unlock Audiobooks](https://support.spotify.com/us/article/audiobooks-purchase/)
  - Voices by INaudio: [Steps to Distribute/Sell an Audiobook with Voices by INaudio](https://voicessupport.inaudio.com/en/articles/3214336)
  - Voices by INaudio: [Digital voice narration (AI narration) FAQs](https://voicessupport.inaudio.com/en/articles/3219456)
  - Voices by INaudio: [Who owns the rights to my uploaded audiobook?](https://voicessupport.inaudio.com/en/articles/3219328)
