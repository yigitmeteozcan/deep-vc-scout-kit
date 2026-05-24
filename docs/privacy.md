# Privacy

This document explains how this repo handles your private fund data.

---

## What stays local

Everything in the `private/` directory is gitignored.

`.gitignore` includes:
```
private/*
!private/.gitkeep
```

The following files never leave your machine unless you explicitly push them:

- `private/pipeline.csv` — your real fund pipeline with company names, status, and notes
- `private/context_pack.md` — the compiled context pack including pipeline company names
- `private/new_candidates.csv` — raw GPT output from your scouting sessions
- `private/deduped_candidates.csv` — dedupe output
- `private/scored_candidates.csv` — scored candidates
- `private/reviewed_candidates.csv` — critic-reviewed candidates
- `private/analyst_notes.md` — meeting-ready notes

**Never commit any of these files to a public or shared repository.**

---

## What is public in this repo

Only template files, example files (with fake/sanitized data), scripts, documentation, and configuration files are tracked in git.

All example files in `examples/` use completely fictional companies and data. No real fund, company, or person is referenced.

---

## Context pack and ChatGPT

When you upload `private/context_pack.md` to a ChatGPT Project:

- The file is sent to OpenAI's servers
- OpenAI's data usage policies apply to this file
- The context pack may include names of companies from your pipeline

**Before uploading the context pack:**

1. Review OpenAI's data usage policy for your account type (personal vs. Team vs. Enterprise)
2. If your fund is bound by confidentiality agreements, check whether uploading company names to a third-party AI service is permitted
3. Consider using only anonymized or fictional company names in `private/pipeline.csv` if full company names are sensitive
4. ChatGPT Team and Enterprise plans typically offer stronger data privacy guarantees — use these if your fund requires it

This repo has no control over how OpenAI stores or uses data uploaded to ChatGPT Projects.

---

## No backend, no API calls

This repo makes zero API calls. All scripts run entirely locally.

No data leaves your machine through this repo. The only external communication is when you manually upload the context pack to ChatGPT — and that is a deliberate action you control.

---

## What to do if you fork this repo publicly

If you fork or clone this repo and make it public:

1. Verify that `private/` is gitignored in your fork before pushing
2. Never commit a real pipeline CSV, even temporarily
3. Never commit a real context pack that includes pipeline company names
4. Replace all template content with sanitized or fictional data before making the repo public
5. Run `git status` to confirm no private files are staged before every commit

---

## Recommended workflow for team use

If multiple analysts on the same fund need to use this toolkit:

- Share the template files and scripts through this repo
- Each analyst maintains their own `private/` directory locally
- Do not sync the `private/` directory through git
- Use a shared internal file store (shared drive, internal wiki) to share context packs if needed — not a public git repo
- Never put real pipeline data in any tracked file

---

## Summary

| Data type | Location | Tracked in git? | Sent to ChatGPT? |
|---|---|---|---|
| Fund thesis (template) | `templates/fund-thesis.md` | Yes (your fill-in) | Only via context pack upload |
| Real pipeline | `private/pipeline.csv` | No — gitignored | Only via context pack upload |
| Context pack | `private/context_pack.md` | No — gitignored | Yes — you upload manually |
| GPT output | `private/new_candidates.csv` | No — gitignored | No |
| Scored/reviewed candidates | `private/*.csv` | No — gitignored | No |
| Analyst notes | `private/analyst_notes.md` | No — gitignored | No |
| Example data | `examples/` | Yes — fake data only | Not automatically |
| Scripts | `scripts/` | Yes | No |
| Documentation | `docs/` | Yes | No |
