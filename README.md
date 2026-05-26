# deep-vc-scout-kit

**Stop restarting your VC scouting brain in every new Deep Research chat.**

---

## The Problem

ChatGPT Deep Research is powerful. But every new chat forgets everything:

- Your fund thesis
- Your existing pipeline
- The startups you already rejected
- What a good fit looks like vs. a bad fit
- Which startup media sources are too obvious
- Which hidden sources you actually trust
- Your geography and sector focus
- Your anti-mainstream filter

The result is the same generic startup list every time. TechCrunch darlings, YC alumni, Crunchbase top results. Things any analyst could find in five minutes.

**This repo fixes that.**

---

## The Solution

Deep VC Scout Kit is a **no-API, local-first toolkit** that helps VC analysts build a reusable scouting brain for ChatGPT Deep Research.

You fill in your fund context once. The repo generates a **GPT Project context pack**. You upload it. Every new Deep Research chat starts from your thesis, your pipeline, your taste, and your source-first scouting rules.

Then local Python scripts handle deduplication, scoring, critic review, and analyst note generation — all without any API keys, subscriptions, or backend.

---

## What This Is Not

| This repo is NOT | This repo IS |
|---|---|
| An autonomous AI scout | A prompt + context toolkit |
| A startup dashboard | A local script workflow |
| A CRM or database | A structured file system |
| An API product | Zero API calls, zero cost |
| A replacement for analyst judgment | A tool to make analyst judgment faster |

**You bring your ChatGPT subscription. The repo brings the structure.**

---

## How It Works

```
fund-thesis.md + pipeline.csv + source rules
          |
          v
  build_context_pack.py
          |
          v
  private/context_pack.md
          |
          v
  Upload to ChatGPT Project
          |
          v
  Run Deep Research with source-first prompt
          |
          v
  GPT returns candidates in CSV format
          |
          v
  Save to private/new_candidates.csv
          |
          v
  dedupe_candidates.py  →  private/deduped_candidates.csv
  score_candidates.py   →  private/scored_candidates.csv
  review_candidates.py  →  private/reviewed_candidates.csv
  generate_notes.py     →  private/analyst_notes.md
```

The most important concept: **source-first scouting.**

Instead of searching "best AI startups in Estonia," the prompt searches source paths:
- Grant winner lists
- University spinout pages
- Demo day PDFs
- Founder hiring posts
- Conference exhibitor lists
- Research commercialization pages
- Corporate innovation challenge finalists

Hidden startups appear in those places before they appear in startup media.

---

## Quickstart

**Step 1: Fill in your fund context**

```bash
# Edit these files with your actual fund details
templates/fund-thesis.md
templates/good-examples.md
templates/bad-examples.md
templates/mainstream-sources-to-avoid.md
templates/hidden-sources-to-prioritize.md
```

**Step 2: Add your existing pipeline (stays local)**

```bash
# Create this file — it is gitignored
private/pipeline.csv
# Minimum columns: company_name,website,status
```

**Step 3: Build the context pack**

```bash
python scripts/build_context_pack.py
```

**Step 4: Upload to ChatGPT Project**

- Create a ChatGPT Project called "Deep VC Scout"
- Upload `private/context_pack.md`
- See `docs/setup-chatgpt-project.md` for instructions

**Step 5: Run Deep Research**

- Open a new chat inside the project
- Paste `gpt-project/deep-research-master-prompt.md`
- GPT will scout source-first and return a CSV

**Step 6: Save GPT output and process it**

```bash
# Paste GPT's CSV output into:
private/new_candidates.csv

# Then run the local pipeline:
python scripts/dedupe_candidates.py
python scripts/score_candidates.py
python scripts/review_candidates.py
python scripts/generate_notes.py
```

**Step 7: Read your analyst notes**

```
private/analyst_notes.md
```

---

## CSV Schema

GPT returns candidates in this format. Your scripts expect the same columns.

| Column | What it contains |
|---|---|
| `company_name` | Company name |
| `website` | Company website URL |
| `source_url` | Exact URL where GPT found the company |
| `short_description` | One sentence: what they do, for whom |
| `founder_signal` | Founder name, background, LinkedIn, or signal |
| `geo_angle` | Geography or diaspora angle |
| `recent_signal` | Most recent activity: launch, hire, grant, pilot |
| `traction_proof` | Customer, revenue, partnership, LOI, grant |
| `why_non_obvious` | Why a mainstream analyst would miss this |
| `why_fund_should_care` | Specific thesis fit |
| `sector` | Sector label |
| `source_type` | Type of source (grant winner, demo day, LinkedIn, etc.) |

---

## Privacy Promise

> Your pipeline stays local. `private/` is gitignored.

The `private/` directory is excluded from git entirely. Your pipeline, context pack, and candidate files never leave your machine unless you push them.

See `docs/privacy.md` for details.

---

## Who This Is For

- **VC analysts** who use Deep Research regularly and want consistent output
- **Solo GPs** who scout without a team
- **Scouts** who cover emerging or niche geographies
- **Accelerator managers** who track deal flow from hidden sources
- **Startup researchers** who want source-first methodology without a paid tool

---

## Requirements

- Python 3.8+ (standard library only, no pip installs)
- A ChatGPT subscription with Deep Research access
- That's it

---

## Repository Structure

```
deep-vc-scout-kit/
├── README.md
├── LICENSE
├── .gitignore
│
├── gpt-project/               # Prompts and instructions for ChatGPT
│   ├── project-instructions.md
│   ├── deep-research-master-prompt.md
│   ├── source-first-scouting-prompt.md
│   ├── anti-mainstream-filter.md
│   └── output-schema.md
│
├── templates/                 # Fill these with your fund context
│   ├── fund-thesis.md
│   ├── pipeline-template.csv
│   ├── good-examples.md
│   ├── bad-examples.md
│   ├── mainstream-sources-to-avoid.md
│   ├── hidden-sources-to-prioritize.md
│   └── scoring-rubric.md
│
├── scripts/                   # Local processing pipeline
│   ├── vc_scout_utils.py
│   ├── build_context_pack.py
│   ├── dedupe_candidates.py
│   ├── score_candidates.py
│   ├── review_candidates.py
│   └── generate_notes.py
│
├── examples/                  # Fake examples to learn from
│   ├── sample-fund-thesis.md
│   ├── sample-pipeline.csv
│   ├── sample-new-candidates.csv
│   ├── sample-context-pack.md
│   ├── sample-reviewed-candidates.csv
│   └── sample-analyst-notes.md
│
├── docs/                      # How-to guides
│   ├── workflow.md
│   ├── setup-chatgpt-project.md
│   ├── customize-for-your-country.md
│   ├── how-to-avoid-mainstream-startups.md
│   └── privacy.md
│
└── private/                   # Gitignored — your real data lives here
    └── .gitkeep
```

---

## Running the Tests

```bash
python -m unittest discover tests
```

---

## License

MIT — see `LICENSE`.

---

*Built for VC analysts who want non-obvious deal flow, not another startup list.*
