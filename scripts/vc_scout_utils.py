"""
Shared helper functions for the deep-vc-scout-kit local processing pipeline.
Uses only Python standard library.
"""

import csv
import difflib
import os
import re
import string


def normalize_company_name(name):
    """
    Return a normalized version of a company name for comparison.
    Lowercases, strips whitespace, removes punctuation, and removes
    common legal suffixes (inc, ltd, llc, corp, gmbh, a.s., a.ş., etc.).
    """
    if not name:
        return ""

    normalized = name.lower().strip()

    # Remove common legal suffixes (with optional trailing dot or comma)
    suffixes = [
        r"\ba\.ş\.?\b",
        r"\ba\.s\.?\b",
        r"\bcorporation\b",
        r"\bcorp\.?\b",
        r"\bincorporated\b",
        r"\binc\.?\b",
        r"\blimited\b",
        r"\bltd\.?\b",
        r"\bllc\.?\b",
        r"\bgmbh\.?\b",
        r"\bplc\.?\b",
        r"\bb\.v\.?\b",
        r"\bs\.a\.?\b",
        r"\bou\b",
        r"\bas\b",
        r"\bab\b",
        r"\boys\b",
        r"\boy\b",
    ]
    for suffix in suffixes:
        normalized = re.sub(suffix, "", normalized)

    # Remove punctuation
    normalized = normalized.translate(str.maketrans("", "", string.punctuation))

    # Collapse multiple spaces
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def clean_domain(url):
    """
    Extract a clean domain from a URL for comparison.
    Strips scheme, www prefix, trailing slash, and path.
    """
    if not url:
        return ""
    url = url.lower().strip()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    url = url.split("/")[0].split("?")[0].split("#")[0]
    return url


def read_csv(path):
    """
    Read a CSV file and return a list of dicts (one per row).
    Returns empty list if file does not exist.
    """
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(path, rows, fieldnames):
    """
    Write a list of dicts to a CSV file with the given fieldnames.
    Creates parent directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def safe_text(value):
    """
    Return the string value, or 'missing' if the value is empty or None.
    """
    if value is None:
        return "missing"
    cleaned = str(value).strip()
    return cleaned if cleaned else "missing"


def ensure_private_dir():
    """
    Create the private/ directory if it does not exist.
    """
    private_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "private")
    os.makedirs(private_dir, exist_ok=True)
    return private_dir


def load_pipeline_names(path):
    """
    Load company names from a pipeline CSV.
    Returns a list of (original_name, normalized_name) tuples.
    """
    rows = read_csv(path)
    names = []
    for row in rows:
        original = row.get("company_name", "").strip()
        if original:
            names.append((original, normalize_company_name(original)))
    return names


def similarity(a, b):
    """
    Return a similarity ratio between two strings using SequenceMatcher.
    Range: 0.0 (no match) to 1.0 (exact match).
    """
    return difflib.SequenceMatcher(None, a, b).ratio()
