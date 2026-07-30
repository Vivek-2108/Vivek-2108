#!/usr/bin/env python3
"""
scripts/config.py

Centralized Configuration for Terminal-Inspired GitHub Profile README.
Single source of truth for handles, links, profile information, and featured projects.
"""

from pathlib import Path

# Base Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SCRIPTS_DIR = ROOT_DIR / "scripts"

# Output Files
CODEFORCES_JSON = DATA_DIR / "codeforces.json"
LEETCODE_JSON = DATA_DIR / "leetcode.json"
CP_STATS_JSON = DATA_DIR / "cp_stats.json"
CP_STATS_SVG = ROOT_DIR / "cp-stats.svg"

# User Profiles & Handles
GITHUB_USERNAME = "vivek-2108"
CODEFORCES_USERNAME = "Code_da_vinci"
CODEFORCES_URL = f"https://codeforces.com/profile/{CODEFORCES_USERNAME}"

LEETCODE_USERNAME = "vivekjadhav07"
LEETCODE_URL = f"https://leetcode.com/u/{LEETCODE_USERNAME}/"

LINKEDIN_URL = "https://www.linkedin.com/in/vivek-jadhav-290a39301/"
EMAIL = "officialvivek5576@gmail.com"
