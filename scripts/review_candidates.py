"""
review_candidates.py

Critic layer: reviews scored candidates for major evidence gaps and
downgrades recommendations where warranted.

Input:  private/scored_candidates.csv
Output: private/reviewed_candidates.csv

Added fields:
    critic_decision         — keep / downgrade / reject
    critic_note             — explanation of critic decision
    missing_evidence        — comma-separated list of missing fields
    final_recommendation    — recommendation after critic review

Downgrade logic:
    Strong Meet -> Meet (if 1+ major gap)
    Meet        -> Watch (if 1+ major gap)
    Watch       -> Pass  (if 2+ major gaps)
    Pass stays Pass

Usage:
    python scripts/review_candidates.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vc_scout_utils import ensure_private_dir, read_csv, safe_text, write_csv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(REPO_ROOT, "private", "scored_candidates.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "private", "reviewed_candidates.csv")

CRITIC_FIELDS = ["critic_decision", "critic_note", "missing_evidence", "final_recommendation"]

# Recommendation order for downgrading
RECOMMENDATION_ORDER = ["Strong Meet", "Meet", "Watch", "Pass"]

MAJOR_GAP_FIELDS = [
    ("founder_signal", "missing founder signal"),
    ("recent_signal", "missing recent signal"),
    ("source_url", "missing source URL"),
    ("traction_proof", "missing traction proof"),
    ("geo_angle", "missing geography/founder angle"),
    ("why_non_obvious", "vague or missing non-obviousness reason"),
    ("why_fund_should_care", "vague or missing fund fit explanation"),
]


def is_missing(value):
    v = safe_text(value)
    return v in ("missing", "") or len(v) < 5


def detect_major_gaps(row):
    gaps = []
    for field, label in MAJOR_GAP_FIELDS:
        if is_missing(row.get(field, "")):
            gaps.append(label)
    return gaps


def downgrade_once(rec):
    if rec not in RECOMMENDATION_ORDER:
        return rec
    idx = RECOMMENDATION_ORDER.index(rec)
    if idx < len(RECOMMENDATION_ORDER) - 1:
        return RECOMMENDATION_ORDER[idx + 1]
    return rec


def review_candidate(row):
    status = row.get("duplicate_status", "no_match")
    current_rec = row.get("recommendation", "Pass")

    # Pass-through for pipeline matches
    if status == "exact_match":
        return {
            "critic_decision": "pass_through",
            "critic_note": "Already in pipeline — not reviewed.",
            "missing_evidence": "",
            "final_recommendation": "already_in_pipeline",
        }

    if status == "possible_match":
        return {
            "critic_decision": "pass_through",
            "critic_note": "Possible pipeline duplicate — manual review required.",
            "missing_evidence": "",
            "final_recommendation": "manual_review_duplicate",
        }

    # Score-based candidates
    gaps = detect_major_gaps(row)
    gap_count = len(gaps)
    missing_str = "; ".join(gaps) if gaps else ""

    if current_rec == "Pass":
        return {
            "critic_decision": "keep",
            "critic_note": f"Pass maintained. {gap_count} major gap(s) noted." if gaps else "Pass maintained.",
            "missing_evidence": missing_str,
            "final_recommendation": "Pass",
        }

    if gap_count == 0:
        return {
            "critic_decision": "keep",
            "critic_note": "No major gaps found. Recommendation maintained.",
            "missing_evidence": "",
            "final_recommendation": current_rec,
        }

    if gap_count >= 3:
        note = f"Rejected by critic: {gap_count} major gap(s) — {missing_str}."
        return {
            "critic_decision": "reject",
            "critic_note": note,
            "missing_evidence": missing_str,
            "final_recommendation": "Pass",
        }

    # 1 or 2 gaps: downgrade once
    final_rec = downgrade_once(current_rec)
    note = f"Downgraded {current_rec} → {final_rec}: {gap_count} major gap(s) — {missing_str}."
    return {
        "critic_decision": "downgrade",
        "critic_note": note,
        "missing_evidence": missing_str,
        "final_recommendation": final_rec,
    }


def main():
    ensure_private_dir()

    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: {INPUT_PATH} not found.")
        print("Run score_candidates.py first.")
        sys.exit(1)

    candidates = read_csv(INPUT_PATH)
    if not candidates:
        print(f"ERROR: {INPUT_PATH} is empty.")
        sys.exit(1)

    base_fields = list(candidates[0].keys())
    for field in CRITIC_FIELDS:
        if field not in base_fields:
            base_fields.append(field)

    output_rows = []
    counts = {
        "keep": 0, "downgrade": 0, "reject": 0,
        "pass_through": 0,
    }

    for candidate in candidates:
        result = review_candidate(candidate)
        candidate.update(result)
        counts[result["critic_decision"]] += 1
        output_rows.append(candidate)

    write_csv(OUTPUT_PATH, output_rows, base_fields)

    print(f"Critic review complete.")
    print(f"  Kept:              {counts['keep']}")
    print(f"  Downgraded:        {counts['downgrade']}")
    print(f"  Rejected:          {counts['reject']}")
    print(f"  Pass-through:      {counts['pass_through']}")
    print(f"  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
