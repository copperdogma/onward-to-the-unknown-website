# Scout 003 - audiobook-and-podcast-distribution-and-elder-friendly-listening

**Source:** Local repo audio surfaces plus current official platform docs
**Scouted:** 2026-04-18
**Scope:** Compare the shipped on-site audiobook and podcast flow against the
strongest external listening lanes that preserve the family-first constraints:
no charging listeners, no paid hosting fees, and minimal friction for mostly
elderly relatives
**Previous:** [Scout 002](scout-002-audiobook-distribution-and-elder-friendly-listening.md)
**Status:** Done

## Decision

- **Recommended canonical listening lane:** keep both audiobook and podcast
  audio canonical on `onward.copper-dog.com` through the existing site-hosted
  MP3 pages and direct download flow.
- **Recommended first external duplicate, if one is later added:** publish one
  public podcast RSS feed from the existing website host, then submit it to
  Apple Podcasts first and Spotify second.
- **Recommended stance on audiobook-specific platforms:** do not make an
  audiobook storefront or audiobook app the next move. None of the researched
  audiobook-specific lanes beats the current site-hosted flow on the combined
  goals of no-charge access, no new hosting spend, no purchase friction, and
  ease for 80+ family listeners.

## Local Baseline

The repo already has the critical family listening substrate:

- `audiobook/manifest.json` maps the reviewed audiobook tracks to the site.
- `podcast/manifest.json` maps the whole-book episode plus chapter episodes to
  the site.
- `make build-family-site` now emits `build/family-site/index.html`,
  `build/family-site/audiobook.html`, `build/family-site/podcast.html`,
  page-level audiobook panels, and page-level podcast panels.
- `scripts/deploy_static_site.py` already publishes the generated site bundle,
  including `audiobook/` and `podcast/` MP3 files, to DreamHost shared hosting.

Fresh local proof in this pass:

- `python -m pytest tests/test_build_family_site.py -q` passed with `25` tests
  on 2026-04-18.
- `make build-family-site` rebuilt the current local output on 2026-04-18 and
  emitted the audio pages plus `_internal/omission-audit.json`.

This means the project does not need a third-party platform to satisfy the
core family goal of "press play here or download an MP3 without confusion."

## Listener-Service Matrix

| Lane | Type | Uses current repo-owned audio? | Recurring hosting fee needed? | Listener friction | Fit for this project |
|---|---|---|---|---|---|
| Current site-hosted audiobook and podcast pages | Canonical lane | Yes | No | Lowest: browser play or direct download, no app required | **Best first lane** |
| Public podcast RSS feed hosted on the site + Apple Podcasts | External duplicate | Yes | No | Low to medium: use Apple Podcasts app, follow once | **Best first external lane** |
| Public podcast RSS feed hosted on the site + Spotify show claim/listing | External duplicate | Yes | No | Medium: Spotify account/app assumptions | Strong secondary duplicate |
| Public RSS feed in Pocket Casts / Overcast / YouTube Music | Listener destination | Yes | No | Medium to high unless the listener already knows the app | Optional convenience, not a launch blocker |
| YouTube RSS ingest | External duplicate | Yes, but converted into static-image videos | No | Medium to high: YouTube setup plus extra moderation surface | Optional later experiment |
| Spotify for Authors audiobook upload | Audiobook storefront | Yes | No upload fee, but requires payment profile | High: purchase/account flow for listeners | Not first |
| Voices by INaudio retail distribution | Audiobook retail network | Not from current MP3s alone; AI titles require LPF workflow | No hosting fee, but more retail/distributor setup | High: retail/library delay and more metadata | Not first |

## Findings

1. **For relatives who already use podcast apps, an open podcast feed is the one external lane that matches the current family constraints** - HIGH value
   Apple allows RSS feeds that are self-generated and self-hosted, and the
   current DreamHost static deploy path already serves public MP3 files. That
   means this project can add a public podcast feed without paying for a
   separate hosting service. Apple Podcasts can index that feed, Spotify can
   claim that feed, Pocket Casts accepts an RSS feed URL or Apple Podcasts
   link, Overcast uses Apple Podcasts for search but still allows direct feed
   URLs, and YouTube Music lets listeners add a podcast by RSS URL.

2. **Apple Podcasts should be the first external target if the project adds a feed** - HIGH value
   Apple’s own creator docs say many people in an audience will be using an
   iPhone and the Apple Podcasts app. Once a listener follows a show, Apple
   Podcasts can automatically download new episodes, notify listeners, and sync
   playback across devices. Apple also says that making a feed public in Apple
   Podcasts Connect exposes it through the Apple Podcasts Catalog API, and
   Overcast explicitly says its search and recommendations rely on Apple
   Podcasts inclusion. That makes Apple the best first directory target for
   older relatives who already live in the Apple ecosystem.

3. **Spotify is the best second external target for podcasts, but it is not a replacement for the website** - HIGH value
   Spotify lets creators claim an existing RSS-fed show with a free Spotify
   account and verifies ownership through the email address in the feed. Spotify
   also makes clear that RSS-based distribution to other platforms is not
   automatic and that each platform still needs to be submitted separately.
   This makes Spotify a worthwhile duplicate because many people already use
   Spotify, but it does not remove the value of the site-hosted play/download
   lane.

4. **YouTube and YouTube Music are real options, but they are not the simplest older-reader lane** - MEDIUM value
   YouTube can ingest an audio-first RSS feed and create static-image videos,
   but that lane is limited to YouTube and YouTube Music, adds another account
   and moderation surface, and does not automatically update re-uploaded audio
   files. Separately, YouTube Music lets individual listeners add a podcast by
   RSS URL directly to their library. That makes YouTube Music a useful
   listener-side fallback for a relative who already uses it, but not the first
   external lane the project should build around.

5. **Dedicated audiobook-platform distribution still adds too much friction for the current family goal** - HIGH value
   Spotify for Authors is free to upload, accepts MP3/WAV/FLAC, and accepts
   digital voice narration, including ElevenLabs. But Spotify also requires a
   payment profile before publishing and treats listener access as an
   audiobook-unlock purchase flow. That is already a worse family experience
   than the website’s direct play/download path.

6. **Voices by INaudio is more capable than the earlier audiobook scout suggested, but still not a first move** - MEDIUM value
   The current INaudio docs now say authors keep their rights, AI-narrated
   titles from ElevenLabs are accepted through LPF files, and some retailers do
   support a list price of `$0.00`. But the same docs also say AI-narrated
   titles are accepted only by select partners, Audible requires an ebook on
   Amazon, Audible does not honor publisher-set free pricing, and retail
   launches can still take weeks. That is too much operational and listener
   complexity for the first family lane.

7. **Spotify’s audiobook docs still drift on availability, which reinforces the case for not making it the primary family path** - LOW value
   Spotify’s availability article currently lists `22` listener markets, while
   the referral-partner article still says audiobooks uploaded through Spotify
   for Authors are available in `14` countries on Spotify. That discrepancy
   does not change the recommendation, but it is another reminder that
   third-party platform rules are a weaker product truth surface than the
   repo-owned website.

## Recommendation

### Canonical Lane

Keep the website as the canonical home for both audio surfaces:

- `audiobook.html` for whole-book and track-by-track listening
- `podcast.html` for whole-book and chapter-episode listening
- page-level `Listen` panels on matching chapters or supplements
- explicit `Download MP3` actions everywhere

The reader-facing copy should continue to say that no app or account is needed.

### First External Duplicate

If the project wants one external lane that helps relatives who already use a
podcast app, the first honest move is:

1. Publish one public podcast RSS feed from `onward.copper-dog.com`
2. Submit that feed to Apple Podcasts
3. Claim that same feed on Spotify

That one feed would also make the show easier to reach from Pocket Casts and
Overcast, and it gives YouTube Music users a direct RSS URL they can add to
their library even if the show is not otherwise indexed there.

**Inference from sources:** Apple’s docs do not explicitly say "this is free,"
but they describe standard RSS-feed submission through Apple Podcasts Connect
separately from the paid Apple Podcasters Program used for subscriptions. Taken
together with the current DreamHost host path, the honest inference is that a
standard public RSS feed can be published without adding paid hosting fees.

### Audiobook-Specific Lane

Do not make an audiobook storefront the next implementation target.

If the project later wants to explore an audiobook duplicate anyway:

- **Spotify for Authors** is the simplest single-service duplicate of the
  current audiobook files, but it still requires a payment profile and puts
  listeners into a purchase/account flow.
- **Voices by INaudio** now looks more flexible than it did in Scout 002, but
  it still requires more metadata, retail decisions, and an LPF-based AI
  narration path for ElevenLabs-origin files.

For older relatives who are simply trying to listen without hassle, the current
site and a later podcast RSS feed still beat these audiobook-platform lanes.

## Required Assets And Metadata

### Current site-hosted lane

- existing audiobook MP3 files and `audiobook/manifest.json`
- existing podcast MP3 files and `podcast/manifest.json`
- page copy that says browser play/download works without an app or account

### Future podcast RSS feed lane

- one public RSS feed URL on `onward.copper-dog.com`
- public episode enclosure URLs pointing at the repo-owned MP3 files
- show artwork
- required RSS metadata including stable GUIDs, titles, descriptions, and
  publish dates
- a public email address in the RSS feed for ownership verification
- Apple-compatible feed structure and validation

### Spotify podcast listing from that feed

- the same RSS feed
- a Spotify account
- access to the verification email address listed in the RSS feed

### Optional YouTube RSS lane

- a YouTube channel in a supported country/region
- show artwork that can be used for static-image episode videos
- willingness to monitor a separate YouTube moderation/copyright surface

### Optional audiobook duplicate later

- **Spotify for Authors**:
  - audiobook files
  - cover art
  - sample file
  - chapter titles
  - payment profile
  - digital voice narration disclosure if the ElevenLabs files are used
- **Voices by INaudio**:
  - LPF export for AI-narrated titles from an accepted provider such as
    ElevenLabs
  - metadata
  - retailer selection
  - price decisions, even if the intended list price is `$0.00`
  - awareness that some retailers will not honor free pricing or AI titles

## Follow-Up Implementation Slice

If the project accepts this recommendation, the next implementation story
should be narrowly scoped to:

- add one public podcast RSS feed emitted from repo-owned metadata
- keep the website as the canonical home and source of media files
- add `Listen in Apple Podcasts` and `Listen in Spotify` actions once those
  listings exist
- optionally provide a plain `Podcast RSS Feed` link for relatives or helpers
  who need to add it manually to Pocket Casts, Overcast, or YouTube Music

That follow-up should stay separate from any audiobook-platform submission
work, because the podcast-feed lane is the cleaner family-utility slice.

## Open Questions

- Does the project want one combined podcast feed that includes both the
  whole-book episode and chapter episodes, or does it want a cleaner
  "whole-book trailer plus chapter feed" structure for app listeners?
- What show artwork should represent the external podcast feed?
- Does the project want a public feed email address dedicated to podcast
  verification and support?
- If a relative specifically asks for an audiobook app instead of a podcast
  app, is that strong enough evidence to revisit Spotify for Authors or INaudio
  later?

## Verification

- `python -m pytest tests/test_build_family_site.py -q`
- `make build-family-site`
- manual review of this scout for plain-language clarity and older-reader fit

## Evidence

- Local repo evidence reviewed:
  - `docs/infrastructure.md`
  - `docs/RUNBOOK.md`
  - `docs/presentation-decisions.md`
  - `audiobook/manifest.json`
  - `podcast/manifest.json`
  - `modules/build_family_site.py`
  - fresh local build output under `build/family-site/`
- Official sources reviewed on 2026-04-18:
  - Apple Podcasts for Creators: [Submit a new show](https://podcasters.apple.com/support/897-submit-a-show)
  - Apple Podcasts for Creators: [Podcast RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements)
  - Apple Podcasts for Creators: [Test your podcast RSS feed](https://podcasters.apple.com/support/828-test-your-podcast)
  - Apple Podcasts for Creators: [Follow on Apple Podcasts](https://podcasters.apple.com/support/3298-follow-on-apple-podcasts)
  - Apple Podcasts for Creators: [Automatic Downloads](https://podcasters.apple.com/support/1662-automatic-downloads-on-apple-podcasts)
  - Spotify for Creators: [Claiming your podcast on Spotify for Creators](https://support.spotify.com/na-en/creators/article/claiming-your-podcast-on-spotify-for-creators/)
  - Spotify for Creators: [Distributing your show to other platforms](https://support.spotify.com/na-en/creators/article/distributing-your-show-to-other-platforms/)
  - Spotify for Creators: [Finding and enabling your RSS feed](https://support.spotify.com/us/creators/article/finding-and-enabling-your-rss-feed/)
  - Spotify for Creators: [Switch your podcast host to Spotify](https://creators.spotify.com/switch)
  - Spotify for Authors: [Uploading audiobooks to Spotify for Authors](https://support.spotify.com/by-en/authors/article/uploading-audiobooks/)
  - Spotify for Authors: [Setting up your payment profile in Spotify for Authors](https://support.spotify.com/mr-en/authors/article/setting-up-spotify-for-authors-payment-profile/)
  - Spotify for Authors: [Digital voice narration](https://support.spotify.com/hn/authors/article/digital-voice-narration/)
  - Spotify for Authors: [Getting your audiobook on other listening platforms](https://support.spotify.com/ad/authors/article/getting-your-audiobook-on-other-listening-platforms/)
  - Spotify for Authors: [Where are audiobooks available on Spotify?](https://support.spotify.com/us/authors/article/audiobooks-availability/)
  - Spotify Support: [Unlock Audiobooks](https://support.spotify.com/us/article/audiobooks-unlock/)
  - Pocket Casts Support: [Submitting Podcasts](https://support.pocketcasts.com/knowledge-base/submitting-podcasts/)
  - Overcast: [Info for Podcasters](https://overcast.fm/podcasterinfo)
  - YouTube Help: [Deliver podcasts using an RSS feed](https://support.google.com/youtube/answer/13525207?hl=en)
  - YouTube Help: [RSS feed delivery available locations](https://support.google.com/youtube/answer/14106258?hl=en)
  - YouTube Music Help: [Add podcasts to your library using RSS feeds](https://support.google.com/youtubemusic/answer/13946190?hl=en)
  - Voices by INaudio: [Digital voice narration (AI narration) FAQs](https://voicessupport.inaudio.com/en/articles/3219456)
  - Voices by INaudio: [Who owns the rights to my uploaded audiobook?](https://voicessupport.inaudio.com/en/articles/3219328)
  - Voices by INaudio: [Can I submit an audiobook even if I don't have an ebook version?](https://voicessupport.inaudio.com/en/articles/3220736)
  - Voices by INaudio: [Can I set a list price of $0?](https://voicessupport.inaudio.com/en/articles/3221184)
