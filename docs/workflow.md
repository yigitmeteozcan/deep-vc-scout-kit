# Full Workflow

This document explains the complete end-to-end workflow for Deep VC Scout Kit.

---

## Step 1: Fill in your fund templates

Start by filling in these files with your real fund context:

**Required:**
- `templates/fund-thesis.md` — your fund's investment thesis, must-haves, hard rejects
- `templates/good-examples.md` — 3-5 companies that represent ideal fund-fit
- `templates/bad-examples.md` — 3-5 companies that represent common bad-fit patterns

**Strongly recommended:**
- `templates/mainstream-sources-to-avoid.md` — startup media and databases to deprioritize in your ecosystem
- `templates/hidden-sources-to-prioritize.md` — grant pages, university spinouts, conference lists to prioritize

**Optional:**
- `templates/scoring-rubric.md` — review and customize the scoring weights if needed

See `examples/sample-fund-thesis.md` for a detailed example.

---

## Step 2: Add your existing pipeline

Create `private/pipeline.csv` with your known companies.

This file is gitignored and never leaves your machine.

Minimum columns: `company_name,website,status`

Full example in `examples/sample-pipeline.csv`.

The dedupe script will use this file to avoid resurfacing companies you already know.

---

## Step 3: Build the context pack

```bash
python scripts/build_context_pack.py
```

This reads all your template files and pipeline data, then writes:

```
private/context_pack.md
```

This is the single file you upload to ChatGPT. It contains your fund thesis, source rules, scoring rubric, good/bad examples, GPT instructions, and known pipeline company names.

Review the output before uploading. Make sure your fund thesis section looks correct.

---

## Step 4: Upload to ChatGPT Project

1. Go to ChatGPT and create a new Project (e.g., "Deep VC Scout — [Your Fund Name]")
2. Upload `private/context_pack.md` to the project
3. See `docs/setup-chatgpt-project.md` for detailed instructions

The context pack becomes the persistent "brain" for every chat in this project.

---

## Step 5: Run Deep Research

1. Open a new chat inside your ChatGPT Project
2. Paste the contents of `gpt-project/deep-research-master-prompt.md`
3. Customize with your target geography, sector focus, and any specific search constraints for this session
4. Start the research

GPT will run source-first scouting missions and return candidates in CSV format.

---

## Step 6: Save GPT output to new_candidates.csv

Copy GPT's CSV output and save it as:

```
private/new_candidates.csv
```

This file is gitignored. Do not commit it.

Make sure the CSV includes the correct column headers. See `gpt-project/output-schema.md` for the required schema.

If GPT returned the output in a different format, paste it and fix the headers manually before running the scripts.

---

## Step 7: Run dedupe

```bash
python scripts/dedupe_candidates.py
```

Input: `private/pipeline.csv` + `private/new_candidates.csv`
Output: `private/deduped_candidates.csv`

This script compares each new candidate against your pipeline using normalized name matching and fuzzy similarity. Each candidate gets a `duplicate_status`:

- `exact_match` — already in pipeline
- `possible_match` — possible duplicate, review manually
- `no_match` — new company, proceed to scoring

---

## Step 8: Run scoring

```bash
python scripts/score_candidates.py
```

Input: `private/deduped_candidates.csv`
Output: `private/scored_candidates.csv`

This script scores each `no_match` candidate on 8 dimensions from the rubric (0, 3, or 5 each, max 40). It generates a `recommendation` field:

- **Strong Meet** (36+)
- **Meet** (30-35)
- **Watch** (22-29)
- **Pass** (<22)

Exact and possible matches are passed through unscored.

---

## Step 9: Run critic review

```bash
python scripts/review_candidates.py
```

Input: `private/scored_candidates.csv`
Output: `private/reviewed_candidates.csv`

This script applies a critic layer that checks for major evidence gaps. It can downgrade a recommendation by one level if 1-2 major gaps are found, or reject a candidate if 3+ major gaps are found.

Major gaps checked:
- missing founder signal
- missing recent signal
- missing source URL
- missing traction proof
- missing geography/founder angle
- vague non-obviousness reason
- vague fund fit explanation

---

## Step 10: Generate analyst notes

```bash
python scripts/generate_notes.py
```

Input: `private/reviewed_candidates.csv`
Output: `private/analyst_notes.md`

This generates meeting-ready notes for all Strong Meet, Meet, and Watch candidates. Pass and duplicate candidates are excluded.

Each note includes:
- What the company does
- Founder / team signal
- Geography angle
- Recent signal
- Traction / proof
- Why the fund should care
- Why others may miss it
- Main risk / missing evidence
- Next action (prioritized by recommendation level)

---

## Full pipeline as one block

```bash
python scripts/build_context_pack.py

# [upload private/context_pack.md to ChatGPT Project]
# [run Deep Research and copy CSV output]
# [save GPT output to private/new_candidates.csv]

python scripts/dedupe_candidates.py
python scripts/score_candidates.py
python scripts/review_candidates.py
python scripts/generate_notes.py
```

Read `private/analyst_notes.md` for your meeting-ready notes.

---

## Repeating the workflow

This workflow is designed to be repeatable:

- Update `private/pipeline.csv` after each scouting session with newly known companies
- Re-run `build_context_pack.py` to refresh the context pack with updated pipeline
- Start a new Deep Research chat with the same project — the brain is already loaded
- Run a new scouting session on a different geography, sector, or source path

The context pack accumulates your learning over time. The more you fill in the templates, the sharper the scouting output becomes.
