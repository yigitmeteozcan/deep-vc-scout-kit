"""
build_context_pack.py

Combines fund thesis, source rules, scoring rubric, examples, GPT instructions,
and known pipeline company names into a single context pack file.

Output: private/context_pack.md

Usage:
    python scripts/build_context_pack.py
"""

import os
import sys

# Allow imports from scripts/ directory
sys.path.insert(0, os.path.dirname(__file__))
from vc_scout_utils import ensure_private_dir, read_csv, safe_text

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES_TO_INCLUDE = [
    ("GPT Project Instructions", "gpt-project/project-instructions.md"),
    ("Source-First Scouting Prompt", "gpt-project/source-first-scouting-prompt.md"),
    ("Anti-Mainstream Filter", "gpt-project/anti-mainstream-filter.md"),
    ("Output Schema", "gpt-project/output-schema.md"),
    ("Fund Thesis", "templates/fund-thesis.md"),
    ("Good Examples", "templates/good-examples.md"),
    ("Bad Examples", "templates/bad-examples.md"),
    ("Mainstream Sources to Avoid", "templates/mainstream-sources-to-avoid.md"),
    ("Hidden Sources to Prioritize", "templates/hidden-sources-to-prioritize.md"),
    ("Scoring Rubric", "templates/scoring-rubric.md"),
]

PIPELINE_PATH = os.path.join(REPO_ROOT, "private", "pipeline.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "private", "context_pack.md")


def read_file(relative_path):
    full_path = os.path.join(REPO_ROOT, relative_path)
    if not os.path.exists(full_path):
        print(f"  WARNING: {relative_path} not found — skipping")
        return None
    with open(full_path, encoding="utf-8") as f:
        return f.read()


def load_known_companies():
    if not os.path.exists(PIPELINE_PATH):
        return []
    rows = read_csv(PIPELINE_PATH)
    names = []
    for row in rows:
        name = safe_text(row.get("company_name", ""))
        if name and name != "missing":
            names.append(name)
    return names


def build_pipeline_section(known_companies):
    if not known_companies:
        return "No pipeline companies loaded. Add private/pipeline.csv to avoid resurfacing known companies.\n"
    lines = ["The following companies are already in the fund's pipeline.",
             "Do not resurface or recommend any of these companies.",
             ""]
    for name in known_companies:
        lines.append(f"- {name}")
    return "\n".join(lines) + "\n"


def main():
    print("Building context pack...")
    ensure_private_dir()

    sections = []

    sections.append("# Deep VC Scout — Context Pack\n")
    sections.append(
        "This file is the scouting brain for this ChatGPT Project. "
        "Read all sections before starting any scouting session.\n"
    )

    # Load and append each source file
    for section_title, relative_path in FILES_TO_INCLUDE:
        content = read_file(relative_path)
        if content:
            sections.append(f"---\n\n# {section_title}\n\n{content}\n")
            print(f"  Included: {relative_path}")

    # Load known pipeline companies
    known_companies = load_known_companies()
    pipeline_section = build_pipeline_section(known_companies)
    sections.append(f"---\n\n# Known Pipeline — Do Not Resurface\n\n{pipeline_section}\n")

    if known_companies:
        print(f"  Included {len(known_companies)} known pipeline companies")
    else:
        print("  No pipeline.csv found — known companies section will be empty")

    # Write output
    full_content = "\n".join(sections)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"\nContext pack created successfully.")
    print(f"  Known companies included: {len(known_companies)}")
    print(f"  Output: {OUTPUT_PATH}")
    print(f"\nNext step: upload {OUTPUT_PATH} to your ChatGPT Project.")


if __name__ == "__main__":
    main()
