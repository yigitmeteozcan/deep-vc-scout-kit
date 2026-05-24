# How to Avoid Mainstream Startups

This guide explains why ChatGPT gives mainstream results by default, and how the source-first methodology fixes that.

---

## Why ChatGPT gives you mainstream startups

When you ask ChatGPT or Deep Research to find "AI startups in Estonia" or "logistics software companies in Turkey," it searches the same places that every analyst already checks:

- TechCrunch and startup news aggregators
- Crunchbase profiles
- YC alumni directories
- Known accelerator portfolio pages
- Public ecosystem maps and startup databases

These are exactly the sources that produce generic deal flow. Every analyst at every fund is querying these sources. If a company appears there, it is already on everyone's radar.

Deep Research is powerful, but it has a default search behavior: it searches by startup category first. That produces mainstream results.

**The problem is not the AI. The problem is the search strategy.**

---

## The source-first solution

Source-first scouting reverses the search order:

**Generic approach (produces mainstream results):**
1. Search startup category keywords
2. Get lists of well-known companies
3. Filter by thesis fit
4. Get the same companies as everyone else

**Source-first approach (produces hidden results):**
1. Search by source path type (grant database, university spinout page, conference exhibitor list)
2. Extract candidate companies from those sources
3. Filter by thesis fit
4. Get companies that haven't appeared in startup media yet

The insight is simple: startups appear in grant recipient lists, university technology transfer pages, and conference exhibitor catalogs months or years before they appear in TechCrunch or Crunchbase. If you search those sources directly, you find the company before the mainstream analyst does.

---

## Concrete examples of the difference

**Mainstream search query:**
```
"best AI startups Estonia 2024"
"mobility startups Turkey"
"top B2B SaaS startups Europe"
"industrial automation software companies Baltics"
```

Result: Companies already covered by startup media, Crunchbase, and every analyst's reading list.

**Source-first search query:**
```
site:taltech.ee "spin-off" OR "spinout" OR "commercialization" 2023 OR 2024
cordis.europa.eu "Estonia" "manufacturing" partner 2024
eit.europa.eu innoEnergy cohort 2024 finalists
[Estonian industry conference] exhibitor list 2024
LinkedIn: "building" "stealth" "hiring" CTO logistics Estonia
```

Result: Companies not yet in any database, found through the exact source that revealed their existence.

---

## The three-step source-first process

**Step 1: Search source paths**
Do not search startup names or categories. Search the types of pages where startups appear before media coverage.

Types of source paths:
- National grant agency recipient lists
- EU program participant databases (Horizon Europe, EIT, EIC)
- University technology transfer office portfolios
- Conference and trade show exhibitor lists (industry events, not startup events)
- Corporate innovation challenge finalist pages
- Founder hiring posts on LinkedIn (especially for senior technical roles)
- Demo day pages for smaller accelerators not tracked by Crunchbase
- Research lab commercialization announcements

**Step 2: Extract candidates from those sources**
For each source path, extract company names, websites, and founder signals. This is where GPT is most useful — it can scan these pages and pull structured data.

**Step 3: Apply the anti-mainstream filter**
For each extracted company, ask:
- Is this company already in mainstream startup media?
- Is this company already on Crunchbase or AngelList?
- Would a normal analyst find this in 5 minutes of Google search?

If yes to any of these, the sourcing edge is partially or fully gone. Note it, but do not assume it's worthless — it depends on the competition for the deal.

---

## How to instruct GPT to search source-first

When running Deep Research, your prompt must explicitly tell GPT to search source paths first.

Use the prompt in `gpt-project/deep-research-master-prompt.md`. It instructs GPT to:
1. Run eight separate search missions, each targeting a specific source type
2. Not start with startup category keywords
3. Record the exact source URL for every candidate found
4. Apply the anti-mainstream test before finalizing the list

Without these explicit instructions, GPT defaults to category keyword search and produces mainstream results.

---

## Why this produces better deal flow

The companies that appear in grant databases, university spinout pages, and conference exhibitor lists are:

- **Earlier stage** — often pre-seed or seed, before institutional investor attention
- **Less competed** — not on multiple VC outreach lists simultaneously
- **More filtered** — grant recipients and accelerator cohorts have been evaluated by domain experts
- **More specific** — they appear in sector-specific sources, not generic startup media
- **More authentic** — the source path is verifiable, not based on a startup's own PR

This is the edge that source-first scouting creates. It is not about AI magic. It is about searching better sources before searching worse ones.

---

## What to do when GPT still returns mainstream startups

If GPT returns a list that includes well-known companies or companies only cited from mainstream media:

1. Check the `source_url` column — if it links to TechCrunch, Crunchbase, or an obvious accelerator portfolio page, the sourcing failed
2. Look at the `source_type` column — if it says "mainstream media" or similar, apply the anti-mainstream filter
3. The `dedupe_candidates.py` and `score_candidates.py` scripts will score these low on `non_obviousness_score`
4. The `review_candidates.py` script will flag missing source URLs and vague non-obviousness reasons as major gaps

If the output is consistently mainstream despite the source-first prompt, ask GPT in a follow-up: "List only companies you found through non-mainstream sources. For each, cite the exact source URL."
