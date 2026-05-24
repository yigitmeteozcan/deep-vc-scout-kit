"""
dedupe_candidates.py

Compares new candidates against the existing pipeline to detect duplicates.

Input:
    private/pipeline.csv       — known companies (company_name required)
    private/new_candidates.csv — GPT output pasted by analyst

Output:
    private/deduped_candidates.csv — all candidates with duplicate_status added

Duplicate status values:
    exact_match      — normalized name matches a pipeline company exactly
    possible_match   — similarity >= 0.85 or one name contains the other
    no_match         — no match found, treat as new company

Usage:
    python scripts/dedupe_candidates.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vc_scout_utils import (
    ensure_private_dir,
    load_pipeline_names,
    normalize_company_name,
    read_csv,
    similarity,
    write_csv,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_PATH = os.path.join(REPO_ROOT, "private", "pipeline.csv")
NEW_CANDIDATES_PATH = os.path.join(REPO_ROOT, "private", "new_candidates.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "private", "deduped_candidates.csv")

SIMILARITY_THRESHOLD = 0.85

OUTPUT_EXTRA_FIELDS = ["duplicate_status", "matched_company_name"]


def check_duplicate(candidate_name, pipeline_names):
    """
    Check a candidate name against all pipeline names.
    Returns (status, matched_name) where status is one of:
        'exact_match', 'possible_match', 'no_match'
    """
    norm_candidate = normalize_company_name(candidate_name)

    if not norm_candidate:
        return "no_match", ""

    for original, norm_pipeline in pipeline_names:
        if not norm_pipeline:
            continue

        # Exact match after normalization
        if norm_candidate == norm_pipeline:
            return "exact_match", original

        # One name contains the other (handles "NordOps" vs "NordOps AI")
        if norm_candidate in norm_pipeline or norm_pipeline in norm_candidate:
            return "possible_match", original

        # Fuzzy similarity
        sim = similarity(norm_candidate, norm_pipeline)
        if sim >= SIMILARITY_THRESHOLD:
            return "possible_match", original

    return "no_match", ""


def main():
    ensure_private_dir()

    if not os.path.exists(NEW_CANDIDATES_PATH):
        print(f"ERROR: {NEW_CANDIDATES_PATH} not found.")
        print("Paste GPT's CSV output into private/new_candidates.csv and run again.")
        sys.exit(1)

    candidates = read_csv(NEW_CANDIDATES_PATH)
    if not candidates:
        print(f"ERROR: {NEW_CANDIDATES_PATH} is empty or has no rows.")
        sys.exit(1)

    pipeline_names = load_pipeline_names(PIPELINE_PATH)
    if not pipeline_names:
        print("WARNING: No pipeline.csv found or it is empty. All candidates will be marked no_match.")

    # Build output fieldnames: original columns + extra fields
    base_fields = list(candidates[0].keys())
    for field in OUTPUT_EXTRA_FIELDS:
        if field not in base_fields:
            base_fields.append(field)

    counts = {"exact_match": 0, "possible_match": 0, "no_match": 0}
    output_rows = []

    for candidate in candidates:
        name = candidate.get("company_name", "").strip()
        status, matched = check_duplicate(name, pipeline_names)
        candidate["duplicate_status"] = status
        candidate["matched_company_name"] = matched
        counts[status] += 1
        output_rows.append(candidate)

    write_csv(OUTPUT_PATH, output_rows, base_fields)

    total = len(output_rows)
    print(f"Dedupe complete.")
    print(f"  Candidates checked:  {total}")
    print(f"  Exact matches:       {counts['exact_match']}")
    print(f"  Possible matches:    {counts['possible_match']}")
    print(f"  New companies:       {counts['no_match']}")
    print(f"  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
