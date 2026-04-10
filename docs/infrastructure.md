# Infrastructure

Operational truth for hosting, DNS, and deployment. Keep this file current when
the real environment changes.

## Hosting

- **Provider**: DreamHost
- **Plan**: `Shared Unlimited`
- **Status**: Confirmed from a user-provided DreamHost account screenshot on
  2026-04-10
- **Observed server label**: `iad1-shared-e1-33`
- **Implication**: Treat the first deploy as `static-export-first` unless new
  evidence shows this project is moving to DreamHost VPS or Dedicated hosting.
- **Verified deploy access on 2026-04-10**:
  - SFTP host: `iad1-shared-e1-33.dreamhost.com`
  - SFTP user: `onward_user`
  - Remote site path: `/home/onward_user/onward.copper-dog.com`
  - Repo-local deploy command: `python scripts/deploy_static_site.py`

## Domain Target

- **Primary public target**: `onward.copper-dog.com`
- **Configured DNS record on 2026-04-10**:
  - type: `A`
  - name: `onward`
  - origin target: `208.113.159.28`
  - Cloudflare proxy: enabled
  - TTL: Auto
- **Observed via SFTP on 2026-04-10**: the remote directory
  `/home/onward_user/onward.copper-dog.com` now serves the staged export bundle
  plus the deploy manifest written by `scripts/deploy_static_site.py`
- **Observed from terminal on 2026-04-10**:
  - `dig +short onward.copper-dog.com` returned Cloudflare edge IPs
    `172.67.217.252` and `104.21.43.33`
  - `curl -I https://onward.copper-dog.com` returned `HTTP/2 200`
  - `curl -I https://onward.copper-dog.com/chapter-001.html` returned
    `HTTP/2 200`
  - `curl -I https://onward.copper-dog.com/images/page-001-000.jpg` returned
    `HTTP/2 200`
  - `curl -I https://onward.copper-dog.com/provenance/blocks.jsonl` returned
    `HTTP/2 200`
  - public page inspection confirmed the homepage contents list and chapter
    page title for the uploaded staged export

## DNS

- **Parent zone**: `copper-dog.com`
- **Observed nameservers on 2026-04-10**:
  - `chelsea.ns.cloudflare.com.`
  - `rick.ns.cloudflare.com.`
- **Current inference**: Cloudflare is the live DNS authority for
  `copper-dog.com`; DreamHost is the hosting provider, not the current public
  DNS authority
- **Origin detail from DreamHost UI**: DreamHost assigned the hosted subdomain
  `onward.copper-dog.com` the origin IP `208.113.159.28`

## Runtime / Deploy Implications

- DreamHost's proxy-backed Node.js and Python app hosting requires Managed VPS
  or Dedicated hosting, not Shared Unlimited.
- A `dreamhosters.com` subdomain is available as a hosted preview surface for
  all DreamHost customers.
- The DreamHost Websites screen shows `copper-dog.com` is already hosted on the
  shared plan, and sibling hosted subdomains already exist under the same
  parent domain.
- For this repo, the safest initial assumption is:
  - build a static site or static export
  - create `onward.copper-dog.com` as another hosted DreamHost subdomain on the
    existing shared account
  - deploy it to DreamHost shared hosting
  - keep `onward.copper-dog.com` routed through Cloudflare to the DreamHost
    origin IP
- The current first deploy path is intentionally thin:
  - local `.env` stores DreamHost credentials and the default source bundle path
  - `scripts/deploy_static_site.py` uploads the contents of that bundle over
    SFTP to `/home/onward_user/onward.copper-dog.com`
  - the script keeps a remote `.deploy-manifest.json` so later deploys can
    remove paths that disappeared from the source bundle
  - the repo-local `/deploy` skill wraps that command and requires public
    hostname verification after upload
  - the current live payload is the staged export bundle
    `input/doc-web-html/story206-onward-proof-r10`

## Sources

- User-provided DreamHost account screenshot captured in this thread on
  2026-04-10
- User-provided DreamHost Websites screenshot captured in this thread on
  2026-04-10 showing `copper-dog.com` hosted on `Shared Unlimited` and existing
  sibling subdomains on the same plan
- User-provided final setup report from a browser-capable agent on 2026-04-10
  stating the Cloudflare record for `onward` points at DreamHost origin IP
  `208.113.159.28` with proxying enabled
- DreamHost Knowledge Base: [Proxy Server](https://help.dreamhost.com/hc/en-us/articles/217955787-Proxy-Server)
- DreamHost Knowledge Base: [Using a dreamhosters.com subdomain](https://help.dreamhost.com/hc/en-us/articles/360002284771-Using-a-dreamhosters-com-subdomain)
- Local verification on 2026-04-10:
  - `dig +short onward.copper-dog.com`
  - `dig +short NS copper-dog.com`
  - `curl -I https://onward.copper-dog.com`

## Open Questions

- Should the project later move Cloudflare SSL mode to Full / Full (Strict)
  once DreamHost origin SSL is provisioned?
