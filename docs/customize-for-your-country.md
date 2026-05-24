# Customize for Your Country

The source-first methodology works for any geography. This guide explains how to customize the toolkit for the country or region you scout.

---

## Why country customization matters

Two things vary by country:

1. **What mainstream sources look like** — every country has its own dominant startup news site, its own well-known accelerator portfolio pages, and its own public startup databases that every analyst already checks.

2. **Where hidden sources hide** — grant databases, university spinout offices, corporate innovation programs, and niche industry events are country-specific.

If you use the default templates without customizing them, GPT will fall back on global mainstream sources and miss the local hidden layer.

---

## How to find mainstream sources to avoid for your country

Ask ChatGPT (not Deep Research — a regular chat is fine):

> "List the most widely-used startup news sites, public startup databases, obvious accelerator portfolio pages, well-known ecosystem maps, and common sourcing tools that most VC analysts covering [your country] would check first when looking for new deals. Include local-language sources."

Then paste the results into `templates/mainstream-sources-to-avoid.md`.

**Example for Estonia:**
- Startup Estonia official directory
- Garage48 and Lift99 community pages
- e-Estonia showcase companies
- Crunchbase Estonian company filter
- Estonian startup media (local equivalents of startup news)
- Well-known accelerator batch pages (Seedcamp, LIFT99 cohorts widely covered)

**Example for Turkey:**
- Major Turkish tech news sites
- Startup Istanbul directory
- TTGV and TÜBİTAK public startup lists (already widely known)
- ITÜ Çekirdek alumni pages (covered by mainstream media)
- Turkish startup databases and ecosystem maps

---

## How to find hidden sources for your country

Ask ChatGPT:

> "List underused, non-obvious, or hard-to-find source paths for startup discovery in [your country]. Include: university technology transfer offices and their URLs, national grant agency recipient databases, niche sector-specific accelerators not widely indexed, corporate innovation challenge programs, industry association events, government R&D project partner lists, and any local sources that a mainstream VC analyst would not typically check."

Then paste the results into `templates/hidden-sources-to-prioritize.md`.

**Example for Estonia:**
- Tallinn University of Technology (TalTech) spinout and research commercialization pages
- Estonian Research Council (ETAg) funded project partner lists
- Enterprise Estonia (EAS) grant recipient announcements
- Business Finland programs (for Finnish-Estonian cross-border companies)
- Horizon Europe Estonian consortium partner pages (on cordis.europa.eu, filtered by EE)
- Specific Estonian industry association annual conference exhibitor lists
- Estonian Defense Industry Association innovation program pages
- Local industry newsletter archives (in Estonian)

**Example for Turkey:**
- TÜBİTAK 1512 and 1507 grant recipient databases
- KOSGEB grant recipient lists (where public)
- Turkish university technology transfer offices (ODTÜ-TTO, İTÜ-TTO, Bilkent TTO)
- Organized Industrial Zone (OSB) technology company directories
- TOBB ETÜ Technopark and other technopark tenant lists
- Turkish defense industry innovation programs (SSB innovation calls)
- Niche Turkish sector newsletters in logistics, manufacturing, energy

---

## How to find diaspora founder signals for your country

Ask ChatGPT:

> "List communities, networks, LinkedIn groups, Slack communities, and online spaces where founders from [your country] who are building companies outside their home country congregate. Also list where founders who moved from [your country] to [target market] announce new ventures."

This helps the scouting prompt find diaspora founders who may be overlooked because they operate in both markets.

---

## Building your customized context pack

1. Fill in `templates/mainstream-sources-to-avoid.md` with your country-specific list
2. Fill in `templates/hidden-sources-to-prioritize.md` with your country-specific hidden sources
3. Run `python scripts/build_context_pack.py`
4. Upload the new `private/context_pack.md` to ChatGPT Project

Now when you run Deep Research, GPT will deprioritize the obvious local sources and start from the hidden layer specific to your ecosystem.

---

## Adding country-specific context to the scouting prompt

When you start a Deep Research session, add a country-specific instruction at the top of the prompt:

```
Country focus for this session: [Your Country]

When running grant/project mission, search specifically:
- [Your country's grant agency] recipient database
- [Your country's EU project portal filter]
- [Specific university TTO pages]

When running conference/exhibitor mission, search specifically:
- [Your country's major industry trade shows]
- [Specific niche events in your sector]

Avoid as primary sources:
- [Your country's mainstream startup news site]
- [Your country's well-known accelerator portfolio pages]
```

The more specific you are about which sources to search and which to avoid, the better GPT's scouting output will be.

---

## Sector-specific customization

The same logic applies to sectors. Ask ChatGPT:

> "What are the non-obvious source paths for finding early-stage [sector] startups in [country]? Include: specialized databases, industry association events, government programs specific to this sector, conference exhibitor lists, and niche newsletters."

Add the results to `templates/hidden-sources-to-prioritize.md` under a sector-specific section.
