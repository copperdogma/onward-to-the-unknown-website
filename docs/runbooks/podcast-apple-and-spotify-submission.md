# Podcast Submission To Apple And Spotify

Checked against current Apple Podcasts and Spotify support docs on April 18,
2026.

This guide is for getting the repo-owned podcast feed onto Apple Podcasts and
Spotify without changing the project’s current model:

- the website stays the canonical listening home
- the podcast feed is the external duplicate
- the audiobook stays on the website only

## What You Are Submitting

- Public podcast page: `https://onward.copper-dog.com/podcast.html`
- Public RSS feed: `https://onward.copper-dog.com/podcast/feed.xml`
- Feed artwork URL: `https://onward.copper-dog.com/podcast/feed-art.png`
- Current public feed email: `cam.marsollier@gmail.com`

The repo currently expects Apple and Spotify listing URLs to be stored later in
`podcast/manifest.json` as top-level `apple_podcasts_url` and `spotify_url`
values after the listings exist.

## Before You Start

1. Make sure the latest site build is deployed publicly, not just built
   locally.
2. Open `https://onward.copper-dog.com/podcast/feed.xml` in a browser and
   confirm it loads.
3. Open `https://onward.copper-dog.com/podcast/feed-art.png` and confirm the
   artwork renders.
4. Decide whether you want the public RSS email to stay
   `cam.marsollier@gmail.com`.

If you want a different public email before submission:

1. Edit `public_contact_email` in [podcast/manifest.json](/Users/cam/.codex/worktrees/cec2/onward-to-the-unknown-website/podcast/manifest.json:1).
2. Rebuild and redeploy the site.
3. Recheck the live feed before continuing.

## Apple Podcasts

### Fast Preflight

Apple recommends testing the feed before submission.

1. On iPhone: open Podcasts, go to `Library`, tap `Edit`, then `Add a Show by URL...`.
2. Or on macOS: open Podcasts, choose `File`, then `Add a Show by URL...`.
3. Paste `https://onward.copper-dog.com/podcast/feed.xml`.
4. Confirm the artwork appears and episodes stream.

Optional direct validation entry:

- [Validate this feed in Apple Podcasts Connect](https://podcastsconnect.apple.com/my-podcasts/new-feed?submitfeed=https://onward.copper-dog.com/podcast/feed.xml)

### Submission Steps

1. Sign in to [Apple Podcasts Connect](https://podcastsconnect.apple.com/).
2. Click `Add (+)` and choose `New Show`.
3. Choose `Add a show with an RSS feed`.
4. Enter `https://onward.copper-dog.com/podcast/feed.xml`.
5. Choose whether to restrict user access inside your Apple Podcasts Connect
   account.
6. Click `Add`.
7. Review the imported show details carefully.
8. Set `Content Rights`.
9. Add show contact information.
10. Open `Availability`.
11. Choose countries or regions.
12. In `Distribution`, decide whether to make the feed publicly available in
    the Apple Podcasts Catalog API.
13. In `Transcripts`, choose whether Apple should generate them or whether you
    will supply them via RSS later.
14. Choose whether to release the show immediately or on a schedule.
15. Save and publish.

### After Apple Approves It

1. Copy the public Apple Podcasts show URL.
2. Add that URL to `podcast/manifest.json` as `apple_podcasts_url`.
3. Rebuild and redeploy the site so the `Listen in Apple Podcasts` button
   appears on `podcast.html`.

Example:

```json
{
  "apple_podcasts_url": "https://podcasts.apple.com/ca/podcast/onward-to-the-unknown-podcast/id1234567890"
}
```

## Spotify

Spotify’s current flow for shows hosted somewhere else is to claim the show in
Spotify for Creators using the RSS feed and an email verification code.

### Claim Steps

1. Sign in to [Spotify for Creators](https://creators.spotify.com/).
2. If this is a new Creators account, choose `Find an existing show`, then
   `Somewhere else`.
3. If you already manage another show there, use `Add a new show`, then
   `Find an existing show`, then `Somewhere else`.
4. Enter `https://onward.copper-dog.com/podcast/feed.xml`.
5. Wait for Spotify to send an 8-digit verification code to the email address
   in the RSS feed.
6. Copy the code from that inbox and paste it into the Spotify claim form.
7. Finish the claim.

### If The Verification Email Does Not Arrive

1. Open the live feed and confirm the `<itunes:email>` value is an inbox you
   can access.
2. Check spam or junk.
3. If you changed the email recently, wait a couple of hours. Spotify says feed
   email updates can take time to propagate.
4. If needed, switch `public_contact_email` in
   [podcast/manifest.json](/Users/cam/.codex/worktrees/cec2/onward-to-the-unknown-website/podcast/manifest.json:1)
   to an inbox you control, rebuild, redeploy, and try again.

### After Spotify Is Claimed

1. Copy the public Spotify show URL.
2. Add that URL to `podcast/manifest.json` as `spotify_url`.
3. Rebuild and redeploy the site so the `Listen in Spotify` button appears on
   `podcast.html`.

Example:

```json
{
  "spotify_url": "https://open.spotify.com/show/abcdef1234567890"
}
```

## Repo Follow-Through After Either Platform Goes Live

Once you have a real Apple or Spotify listing URL:

1. Update [podcast/manifest.json](/Users/cam/.codex/worktrees/cec2/onward-to-the-unknown-website/podcast/manifest.json:1).
2. Run:

```bash
make build-family-site
```

3. Deploy the refreshed site with the normal repo deploy flow.
4. Open `https://onward.copper-dog.com/podcast.html` and confirm the new
   button appears.
5. Open the platform listing and confirm the feed, art, and episode ordering
   look right.

If both are live, the top of the manifest should look roughly like this:

```json
{
  "feed_path": "podcast/feed.xml",
  "public_contact_email": "cam@example.com",
  "artwork_path": "feed-art.png",
  "artwork_output_path": "podcast/feed-art.png",
  "apple_podcasts_url": "https://podcasts.apple.com/ca/podcast/onward-to-the-unknown-podcast/id1234567890",
  "spotify_url": "https://open.spotify.com/show/abcdef1234567890"
}
```

## Recommended Order

1. Deploy the latest site build.
2. Test the feed in Apple Podcasts.
3. Submit the feed to Apple Podcasts.
4. Claim the same feed on Spotify.
5. Add the resulting Apple and Spotify URLs back into `podcast/manifest.json`.
6. Rebuild and redeploy so the site shows the real platform buttons.

## Official Sources

- Apple: [Podcast RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements)
- Apple: [Show Cover](https://podcasters.apple.com/support/5514-show-cover-template)
- Apple: [Validate your podcast RSS feed](https://podcasters.apple.com/support/829-validate-your-podcast)
- Apple: [Test your podcast RSS feed](https://podcasters.apple.com/support/828-test-your-podcast)
- Apple: [Submit a new show](https://podcasters.apple.com/support/897-submit-a-show)
- Spotify: [Claiming your podcast on Spotify for Creators](https://support.spotify.com/np-en/creators/article/claiming-your-podcast-on-spotify-for-creators/)
- Spotify: [Adding your email address to your RSS feed](https://support.spotify.com/cm-en/creators/article/adding-your-email-address-to-your-rss-feed/)
- Spotify: [Distributing your show to other platforms](https://support.spotify.com/si-en/creators/article/distributing-your-show-to-other-platforms/)
