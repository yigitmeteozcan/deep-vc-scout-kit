"""
score_candidates.py

Scores new candidates (no_match) from the dedupe output using the VC rubric.
Candidates marked exact_match or possible_match are passed through unscored.

Input:  private/deduped_candidates.csv
Output: private/scored_candidates.csv

Scoring dimensions (0, 3, or 5 each, max total 40):
    team_score
    product_score
    technology_score
    commercialization_score
    fund_fit_score
    geo_angle_score
    non_obviousness_score
    recency_signal_score

Recommendations:
    36+     Strong Meet
    30-35   Meet
    22-29   Watch
    <22     Pass

Usage:
    python scripts/score_candidates.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vc_scout_utils import ensure_private_dir, read_csv, safe_text, write_csv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(REPO_ROOT, "private", "deduped_candidates.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "private", "scored_candidates.csv")

SCORE_FIELDS = [
    "team_score",
    "product_score",
    "technology_score",
    "commercialization_score",
    "fund_fit_score",
    "geo_angle_score",
    "non_obviousness_score",
    "recency_signal_score",
    "total_score",
    "recommendation",
    "scoring_note",
]

# Keywords that suggest buzzword-only claims (score penalty triggers)
BUZZWORD_ONLY = [
    "ai-powered platform",
    "ai platform for enterprise",
    "next-generation",
    "state-of-the-art",
    "digital transformation",
    "disruptive innovation",
    "cutting-edge",
    "blockchain-based platform",
]

# Keywords that suggest real technical depth
DEEP_TECH_SIGNALS = [
    "robotics", "hardware", "sensor", "firmware", "embedded", "industrial automation",
    "energy storage", "battery", "materials", "synthetic biology", "manufacturing",
    "simulation", "ml model", "inference", "computer vision", "lidar", "radar",
    "autonomous", "drone", "satellite", "propulsion", "chemistry", "ai infrastructure",
    "semiconductor", "photonics", "quantum",
]

# Source types that indicate hidden discovery
HIDDEN_SOURCE_TYPES = [
    "grant winner", "eu project", "university spinout", "demo day", "conference exhibitor",
    "linkedin", "hiring post", "accelerator finalist", "corporate innovation",
    "niche newsletter", "research lab", "industry association", "stealth",
]

# Source types that indicate mainstream discovery
MAINSTREAM_SOURCE_TYPES = [
    "techcrunch", "crunchbase", "angellist", "ycombinator", "yc", "sifted",
    "eu-startups", "techeu", "producthunt", "forbes",
]


def is_missing(value):
    v = safe_text(value)
    return v in ("missing", "") or len(v) < 5


def has_buzzword_only(text):
    text_lower = text.lower()
    return any(bw in text_lower for bw in BUZZWORD_ONLY)


def has_deep_tech(text):
    text_lower = text.lower()
    return any(signal in text_lower for signal in DEEP_TECH_SIGNALS)


def is_hidden_source(source_type):
    st = safe_text(source_type).lower()
    return any(h in st for h in HIDDEN_SOURCE_TYPES)


def is_mainstream_source(source_type):
    st = safe_text(source_type).lower()
    return any(m in st for m in MAINSTREAM_SOURCE_TYPES)


def score_team(row):
    signal = safe_text(row.get("founder_signal", ""))
    if is_missing(signal):
        return 0
    # Strong signals: LinkedIn URL, PhD, repeat founder, named company
    strong = any(kw in signal.lower() for kw in [
        "linkedin", "phd", "dr.", "cto", "ceo", "co-founder", "serial",
        "repeat", "former", "previously", "spun out", "professor",
    ])
    if strong and len(signal) > 30:
        return 5
    return 3


def score_product(row):
    desc = safe_text(row.get("short_description", ""))
    if is_missing(desc):
        return 0
    if has_buzzword_only(desc) and not has_deep_tech(desc):
        return 0
    # Specific buyer + workflow = higher score
    specific = any(kw in desc.lower() for kw in [
        "for ", "enables ", "helps ", "replaces ", "automates ", "manages ",
        "tracks ", "monitors ", "schedules ", "reduces ", "increases ",
    ])
    if specific and len(desc) > 40:
        return 5
    return 3


def score_technology(row):
    desc = safe_text(row.get("short_description", ""))
    non_obvious = safe_text(row.get("why_non_obvious", ""))
    combined = f"{desc} {non_obvious}".lower()
    if has_deep_tech(combined):
        return 5
    if has_buzzword_only(combined) and not has_deep_tech(combined):
        return 0
    return 3


def score_commercialization(row):
    traction = safe_text(row.get("traction_proof", ""))
    if is_missing(traction):
        return 0
    strong = any(kw in traction.lower() for kw in [
        "paying", "revenue", "arr", "mrr", "customer", "signed", "contract",
        "partnership", "strategic", "€", "$", "eur", "usd",
    ])
    if strong:
        return 5
    some = any(kw in traction.lower() for kw in [
        "pilot", "grant", "accelerator", "loi", "letter of intent",
        "accepted", "selected", "cohort", "proof of concept",
    ])
    if some:
        return 3
    return 0


def score_fund_fit(row):
    fit_text = safe_text(row.get("why_fund_should_care", ""))
    if is_missing(fit_text):
        return 0
    if len(fit_text) > 60:
        return 5
    return 3


def score_geo_angle(row):
    geo = safe_text(row.get("geo_angle", ""))
    if is_missing(geo):
        return 0
    if len(geo) > 20:
        return 5
    return 3


def score_non_obviousness(row):
    source_type = safe_text(row.get("source_type", ""))
    why = safe_text(row.get("why_non_obvious", ""))
    if is_mainstream_source(source_type):
        return 0
    if is_hidden_source(source_type) and not is_missing(why):
        return 5
    if not is_missing(why) and len(why) > 30:
        return 3
    return 0


def score_recency(row):
    recent = safe_text(row.get("recent_signal", ""))
    if is_missing(recent):
        return 0
    # Very recent: keywords suggesting last 12 months
    very_recent = any(kw in recent.lower() for kw in [
        "2024", "2025", "q1", "q2", "q3", "q4", "january", "february", "march",
        "april", "may", "june", "july", "august", "september", "october",
        "november", "december", "last month", "this year", "recently",
    ])
    if very_recent:
        return 5
    return 3


def recommendation(total):
    if total >= 36:
        return "Strong Meet"
    if total >= 30:
        return "Meet"
    if total >= 22:
        return "Watch"
    return "Pass"


def build_scoring_note(scores, row):
    notes = []
    if scores["team_score"] == 0:
        notes.append("no founder evidence")
    if scores["product_score"] == 0:
        notes.append("vague or buzzword product description")
    if scores["technology_score"] == 0:
        notes.append("no technical differentiation evident")
    if scores["commercialization_score"] == 0:
        notes.append("no traction or proof")
    if scores["fund_fit_score"] == 0:
        notes.append("no specific fund fit explanation")
    if scores["geo_angle_score"] == 0:
        notes.append("no geography/founder angle")
    if scores["non_obviousness_score"] == 0:
        notes.append("mainstream source or no non-obviousness reason")
    if scores["recency_signal_score"] == 0:
        notes.append("no recent signal")
    if not notes:
        return "Sufficient evidence across most dimensions."
    return "Low evidence: " + "; ".join(notes) + "."


def score_candidate(row):
    scores = {
        "team_score": score_team(row),
        "product_score": score_product(row),
        "technology_score": score_technology(row),
        "commercialization_score": score_commercialization(row),
        "fund_fit_score": score_fund_fit(row),
        "geo_angle_score": score_geo_angle(row),
        "non_obviousness_score": score_non_obviousness(row),
        "recency_signal_score": score_recency(row),
    }
    total = sum(scores.values())
    scores["total_score"] = total
    scores["recommendation"] = recommendation(total)
    scores["scoring_note"] = build_scoring_note(scores, row)
    return scores


def main():
    ensure_private_dir()

    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: {INPUT_PATH} not found.")
        print("Run dedupe_candidates.py first.")
        sys.exit(1)

    candidates = read_csv(INPUT_PATH)
    if not candidates:
        print(f"ERROR: {INPUT_PATH} is empty.")
        sys.exit(1)

    base_fields = list(candidates[0].keys())
    for field in SCORE_FIELDS:
        if field not in base_fields:
            base_fields.append(field)

    output_rows = []
    counts = {"scored": 0, "skipped_duplicate": 0, "skipped_possible": 0}

    for candidate in candidates:
        status = candidate.get("duplicate_status", "no_match")

        if status == "exact_match":
            candidate["recommendation"] = "already_in_pipeline"
            candidate["scoring_note"] = "Exact pipeline match — skip."
            for field in SCORE_FIELDS:
                if field not in candidate:
                    candidate[field] = ""
            counts["skipped_duplicate"] += 1

        elif status == "possible_match":
            candidate["recommendation"] = "manual_review_duplicate"
            candidate["scoring_note"] = (
                f"Possible pipeline match with '{candidate.get('matched_company_name', '')}' — verify manually."
            )
            for field in SCORE_FIELDS:
                if field not in candidate:
                    candidate[field] = ""
            counts["skipped_possible"] += 1

        else:
            scores = score_candidate(candidate)
            candidate.update(scores)
            counts["scored"] += 1

        output_rows.append(candidate)

    write_csv(OUTPUT_PATH, output_rows, base_fields)

    print(f"Scoring complete.")
    print(f"  Scored (new companies):      {counts['scored']}")
    print(f"  Skipped (exact duplicates):  {counts['skipped_duplicate']}")
    print(f"  Skipped (possible matches):  {counts['skipped_possible']}")
    print(f"  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
