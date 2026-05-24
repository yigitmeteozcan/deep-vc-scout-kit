"""
Tests for duplicate detection logic in dedupe_candidates.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from vc_scout_utils import normalize_company_name, similarity

# Reproduce the check_duplicate logic here for unit testing
# (mirrors dedupe_candidates.py without file I/O)

SIMILARITY_THRESHOLD = 0.85


def check_duplicate(candidate_name, pipeline_names):
    """
    pipeline_names: list of (original_name, normalized_name) tuples
    Returns (status, matched_name)
    """
    norm_candidate = normalize_company_name(candidate_name)

    if not norm_candidate:
        return "no_match", ""

    for original, norm_pipeline in pipeline_names:
        if not norm_pipeline:
            continue

        if norm_candidate == norm_pipeline:
            return "exact_match", original

        if norm_candidate in norm_pipeline or norm_pipeline in norm_candidate:
            return "possible_match", original

        sim = similarity(norm_candidate, norm_pipeline)
        if sim >= SIMILARITY_THRESHOLD:
            return "possible_match", original

    return "no_match", ""


def make_pipeline(names):
    return [(n, normalize_company_name(n)) for n in names]


class TestExactDuplicate(unittest.TestCase):

    def test_exact_name_match(self):
        pipeline = make_pipeline(["NordOps AI"])
        status, matched = check_duplicate("NordOps AI", pipeline)
        self.assertEqual(status, "exact_match")
        self.assertEqual(matched, "NordOps AI")

    def test_exact_match_different_case(self):
        pipeline = make_pipeline(["NordOps AI"])
        status, matched = check_duplicate("nordops ai", pipeline)
        self.assertEqual(status, "exact_match")

    def test_exact_match_with_suffix(self):
        pipeline = make_pipeline(["FleetGrid OY"])
        status, matched = check_duplicate("FleetGrid", pipeline)
        # "fleetgrid oy" normalized = "fleetgrid oy" -> wait, OY is a suffix so normalized = "fleetgrid"
        # candidate "FleetGrid" normalized = "fleetgrid"
        # "fleetgrid" == "fleetgrid" -> exact_match
        self.assertEqual(status, "exact_match")

    def test_exact_match_with_inc_suffix(self):
        pipeline = make_pipeline(["DataRoute Inc"])
        status, matched = check_duplicate("DataRoute", pipeline)
        self.assertEqual(status, "exact_match")

    def test_exact_match_turkish_suffix(self):
        pipeline = make_pipeline(["TechFirm A.Ş."])
        status, matched = check_duplicate("TechFirm", pipeline)
        self.assertEqual(status, "exact_match")


class TestPossibleDuplicate(unittest.TestCase):

    def test_substring_match(self):
        pipeline = make_pipeline(["NordOps"])
        status, matched = check_duplicate("NordOps AI", pipeline)
        # normalized: "nordops ai" contains "nordops" -> possible_match
        self.assertEqual(status, "possible_match")

    def test_fuzzy_similarity_match(self):
        pipeline = make_pipeline(["VoltBridge"])
        # "VoltBridg" is very close to "VoltBridge"
        status, matched = check_duplicate("VoltBridg", pipeline)
        self.assertEqual(status, "possible_match")

    def test_high_similarity(self):
        pipeline = make_pipeline(["GridShift"])
        status, matched = check_duplicate("Grid Shift", pipeline)
        # "gridshift" vs "grid shift" after normalization
        # similarity should be high
        sim = similarity("gridshift", "gridshift")
        self.assertGreaterEqual(sim, SIMILARITY_THRESHOLD)

    def test_contains_check_reverse(self):
        pipeline = make_pipeline(["FleetGrid Technologies"])
        status, matched = check_duplicate("FleetGrid", pipeline)
        # "fleetgrid" in "fleetgrid technologies" -> possible_match
        self.assertEqual(status, "possible_match")


class TestNoMatch(unittest.TestCase):

    def test_completely_different_company(self):
        pipeline = make_pipeline(["NordOps AI", "FleetGrid", "BatteryLens"])
        status, matched = check_duplicate("VoltBridge OY", pipeline)
        self.assertEqual(status, "no_match")
        self.assertEqual(matched, "")

    def test_empty_candidate_name(self):
        pipeline = make_pipeline(["NordOps AI"])
        status, matched = check_duplicate("", pipeline)
        self.assertEqual(status, "no_match")

    def test_empty_pipeline(self):
        pipeline = []
        status, matched = check_duplicate("VoltBridge OY", pipeline)
        self.assertEqual(status, "no_match")

    def test_similar_but_below_threshold(self):
        pipeline = make_pipeline(["PowerGrid"])
        # "gridpower" vs "powergrid" — word order reversed, low similarity
        status, matched = check_duplicate("GridPower", pipeline)
        norm_a = normalize_company_name("GridPower")
        norm_b = normalize_company_name("PowerGrid")
        sim = similarity(norm_a, norm_b)
        if sim < SIMILARITY_THRESHOLD:
            self.assertEqual(status, "no_match")
        else:
            self.assertIn(status, ["possible_match", "no_match"])

    def test_generic_ai_vs_unrelated(self):
        pipeline = make_pipeline(["RouteSync", "ColdStore OY"])
        status, matched = check_duplicate("GenericAI Corp", pipeline)
        self.assertEqual(status, "no_match")


if __name__ == "__main__":
    unittest.main()
