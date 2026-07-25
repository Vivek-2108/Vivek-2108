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
ASSETS_DIR = ROOT_DIR / "assets"
SCRIPTS_DIR = ROOT_DIR / "scripts"

# Output Files
CONTRIBUTIONS_JSON = DATA_DIR / "contributions.json"
CODEFORCES_JSON = DATA_DIR / "codeforces.json"
LEETCODE_JSON = DATA_DIR / "leetcode.json"
CP_STATS_JSON = DATA_DIR / "cp_stats.json"

ASCII_SVG = ROOT_DIR / "ascii.svg"
INFO_CARD_SVG = ROOT_DIR / "info-card.svg"
HEATMAP_SVG = ROOT_DIR / "contrib-heatmap.svg"
CP_STATS_SVG = ROOT_DIR / "cp-stats.svg"

# User Profiles & Handles
GITHUB_USERNAME = "Vivek-2108"
CODEFORCES_USERNAME = "Code_da_vinci"
CODEFORCES_URL = f"https://codeforces.com/profile/{CODEFORCES_USERNAME}"

LEETCODE_USERNAME = "vivekjadhav07"
LEETCODE_URL = f"https://leetcode.com/u/{LEETCODE_USERNAME}/"

LINKEDIN_URL = "https://www.linkedin.com/in/vivek-jadhav-290a39301/"

# Information Card Data (Neofetch Terminal Card)
PROFILE_DATA = {
    "name": "Vivek Jadhav",
    "role": "Full Stack & Android Developer",
    "current_project": "Terminal Profile Automation & AI Systems",
    "languages": "Java, Python, JavaScript, TypeScript, SQL",
    "backend": "Java, Node.js, Express, REST APIs, Firebase",
    "frontend": "React, Angular, HTML5, CSS3, SVG",
    "devops": "Git, GitHub Actions, Linux, Vercel",
    "database": "MySQL, MongoDB, Supabase",
    "interests": "Competitive Programming, Web Dev & DSA",
}

# Featured Projects
FEATURED_PROJECTS = [
    {
        "name": "Terminal Profile README Engine",
        "description": "Autonomous vector graphics profile generator with daily automated data pipelines.",
        "tech": "Python, SVG, GitHub Actions, Web Scraping",
        "link": f"https://github.com/{GITHUB_USERNAME}/{GITHUB_USERNAME}",
    },
    {
        "name": "Android & Web Applications",
        "description": "Full-stack mobile & web applications focused on performance and modern design.",
        "tech": "Java, React, Node.js, Firebase",
        "link": f"https://github.com/{GITHUB_USERNAME}?tab=repositories",
    },
]
