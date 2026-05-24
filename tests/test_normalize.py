"""
Tests for normalize_company_name in vc_scout_utils.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from vc_scout_utils import normalize_company_name


class TestNormalizeCompanyName(unittest.TestCase):

    def test_lowercase(self):
        self.assertEqual(normalize_company_name("NORDOPS AI"), "nordops ai")

    def test_trim_whitespace(self):
        self.assertEqual(normalize_company_name("  FleetGrid  "), "fleetgrid")

    def test_remove_punctuation(self):
        self.assertEqual(normalize_company_name("Volt-Bridge"), "voltbridge")
        self.assertEqual(normalize_company_name("Grid.Works"), "gridworks")

    def test_suffix_inc(self):
        self.assertEqual(normalize_company_name("NordOps Inc."), "nordops")
        self.assertEqual(normalize_company_name("NordOps Inc"), "nordops")

    def test_suffix_ltd(self):
        self.assertEqual(normalize_company_name("FleetGrid Ltd."), "fleetgrid")
        self.assertEqual(normalize_company_name("FleetGrid Ltd"), "fleetgrid")

    def test_suffix_llc(self):
        self.assertEqual(normalize_company_name("DataRoute LLC"), "dataroute")

    def test_suffix_corp(self):
        self.assertEqual(normalize_company_name("TechCore Corp"), "techcore")
        self.assertEqual(normalize_company_name("TechCore Corporation"), "techcore")

    def test_suffix_gmbh(self):
        self.assertEqual(normalize_company_name("AutoWerk GmbH"), "autowerk")

    def test_suffix_plc(self):
        self.assertEqual(normalize_company_name("GridStar PLC"), "gridstar")

    def test_suffix_as(self):
        self.assertEqual(normalize_company_name("NordShip AS"), "nordship")

    def test_suffix_oy(self):
        self.assertEqual(normalize_company_name("VoltBridge OY"), "voltbridge")
        self.assertEqual(normalize_company_name("VoltBridge OYS"), "voltbridge")

    def test_suffix_turkish_as(self):
        self.assertEqual(normalize_company_name("TechFirm A.Ş."), "techfirm")
        self.assertEqual(normalize_company_name("TechFirm A.S."), "techfirm")
        self.assertEqual(normalize_company_name("TechFirm A.Ş"), "techfirm")

    def test_empty_string(self):
        self.assertEqual(normalize_company_name(""), "")

    def test_none(self):
        self.assertEqual(normalize_company_name(None), "")

    def test_combined_punctuation_and_suffix(self):
        result = normalize_company_name("Grid-Works Inc.")
        self.assertEqual(result, "gridworks")

    def test_name_with_numbers(self):
        result = normalize_company_name("Route24 OY")
        self.assertEqual(result, "route24")


if __name__ == "__main__":
    unittest.main()
