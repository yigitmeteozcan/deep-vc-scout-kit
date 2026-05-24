"""
generate_notes.py

Generates analyst-ready meeting notes from reviewed candidates.

Only includes: Strong Meet, Meet, Watch
Skips: Pass, already_in_pipeline, manual_review_duplicate

Input:  private/reviewed_candidates.csv
Output: private/analyst_notes.md

Usage:
    python scripts/generate_notes.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vc_scout_utils import ensure_private_dir, read_csv, safe_text

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(REPO_ROOT, "private", "reviewed_candidates.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "private", "analyst_notes.md")

INCLUDE_RECOMMENDATIONS = {"Strong Meet", "Meet", "Watch"}

NEXT_ACTION = {
    "Strong Meet": "Request intro or reach out directly. Prioritize within this week.",
    "Meet": "Schedule exploratory call. Review website and LinkedIn before meeting.",
    "Watch": "Monitor for traction update or team news. Revisit in 30-60 days.",
}


def format_note(row):
    name = safe_text(row.get("company_name", ""))
    rec = safe_text(row.get("final_recommendation", ""))
    what = safe_text(row.get("short_description", ""))
    founder = safe_text(row.get("founder_signal", ""))
    geo = safe_text(row.get("geo_angle", ""))
    recent = safe_text(row.get("recent_signal", ""))
    traction = safe_text(row.get("traction_proof", ""))
    fund_care = safe_text(row.get("why_fund_should_care", ""))
    non_obvious = safe_text(row.get("why_non_obvious", ""))
    missing = safe_text(row.get("missing_evidence", ""))
    website = safe_text(row.get("website", ""))
    source = safe_text(row.get("source_url", ""))
    next_action = NEXT_ACTION.get(rec, "Review further before deciding.")

    website_line = f"Website: {website}" if website != "missing" else "Website: missing"
    source_line = f"Source: {source}" if source != "missing" else "Source: missing"

    risk_note = missing if missing and missing != "missing" else "No major gaps flagged."

    lines = [
        f"## {name}",
        f"",
        f"**Recommendation:** {rec}",
        f"",
        f"{website_line}  ",
        f"{source_line}",
        f"",
        f"**What they do:** {what}",
        f"",
        f"**Founder / team signal:** {founder}",
        f"",
        f"**Geography / founder angle:** {geo}",
        f"",
        f"**Recent signal:** {recent}",
        f"",
        f"**Traction / proof:** {traction}",
        f"",
        f"**Why the fund should care:** {fund_care}",
        f"",
        f"**Why others may miss it:** {non_obvious}",
        f"",
        f"**Main risk / missing evidence:** {risk_note}",
        f"",
        f"**Next action:** {next_action}",
        f"",
        "---",
        "",
    ]
    return "\n".join(lines)


def main():
    ensure_private_dir()

    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: {INPUT_PATH} not found.")
        print("Run review_candidates.py first.")
        sys.exit(1)

    candidates = read_csv(INPUT_PATH)
    if not candidates:
        print(f"ERROR: {INPUT_PATH} is empty.")
        sys.exit(1)

    included = []
    for candidate in candidates:
        rec = safe_text(candidate.get("final_recommendation", ""))
        if rec in INCLUDE_RECOMMENDATIONS:
            included.append(candidate)

    if not included:
        print("No candidates with Strong Meet, Meet, or Watch recommendation found.")
        print("Nothing written to analyst_notes.md.")
        return

    # Sort by recommendation priority
    order = {"Strong Meet": 0, "Meet": 1, "Watch": 2}
    included.sort(key=lambda r: order.get(safe_text(r.get("final_recommendation", "")), 99))

    sections = [
        "# Analyst Notes\n",
        f"Generated from `reviewed_candidates.csv`  \n",
        f"Total candidates in notes: {len(included)}\n",
        "\n---\n",
    ]

    # Summary table
    sections.append("## Summary\n")
    sections.append("| Company | Recommendation | Sector | Website |")
    sections.append("|---|---|---|---|")
    for row in included:
        name = safe_text(row.get("company_name", ""))
        rec = safe_text(row.get("final_recommendation", ""))
        sector = safe_text(row.get("sector", ""))
        website = safe_text(row.get("website", ""))
        sections.append(f"| {name} | {rec} | {sector} | {website} |")
    sections.append("\n---\n")

    # Individual notes
    sections.append("## Candidate Notes\n")
    for row in included:
        sections.append(format_note(row))

    content = "\n".join(sections)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Analyst notes generated.")
    print(f"  Candidates included: {len(included)}")
    for row in included:
        name = safe_text(row.get("company_name", ""))
        rec = safe_text(row.get("final_recommendation", ""))
        print(f"    {rec}: {name}")
    print(f"  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
