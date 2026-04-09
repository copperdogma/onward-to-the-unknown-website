# Onward to the Unknown Website

This repo is the home for the public-facing website built around *Onward to the
Unknown* and its surrounding family-archive materials.

`doc-web` remains the upstream processing tool for the book itself. This repo
owns the website-specific layer:

- import or consume the processed book output
- normalize it into a site-friendly content model
- connect book chapters to companion media and scans
- present the material as a durable, navigable family archive site

Current upstream reference:

- [`/Users/cam/Documents/Projects/doc-web`](/Users/cam/Documents/Projects/doc-web)

## Bootstrap Surface

This repo is currently bootstrapped with the shared methodology package and
imported skill surface from `doc-web`.

Useful commands:

```bash
make skills-sync
make methodology-compile
make methodology-check
```

## Current State

The methodology package is installed, but the site runtime has not been chosen
yet. The next substantive work should define:

1. the import contract from `doc-web`
2. the canonical content/data model for the website
3. the first end-to-end website slice for one chapter plus linked media

