#!/usr/bin/env python3
"""
scripts/fetch_contributions.py

Scrapes GitHub contribution data directly from https://github.com/users/<username>/contributions
without requiring GitHub tokens or third-party APIs.
Saves extracted calendar data and streak metrics to data/contributions.json.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Paths and Constants
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_JSON = DATA_DIR / "contributions.json"

USERNAME = "vivekjadhav07"
CONTRIBUTIONS_URL = f"https://github.com/users/{USERNAME}/contributions"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def calculate_streaks(days_data: list[dict]) -> tuple[int, int]:
    """Calculate longest streak and current streak from sorted daily contribution records."""
    if not days_data:
        return 0, 0

    # Ensure days are sorted chronologically
    sorted_days = sorted(days_data, key=lambda d: d["date"])

    # Calculate longest streak
    longest_streak = 0
    current_temp = 0
    for day in sorted_days:
        if day["count"] > 0:
            current_temp += 1
            if current_temp > longest_streak:
                longest_streak = current_temp
        else:
            current_temp = 0

    # Calculate current active streak
    current_streak = 0
    idx = len(sorted_days) - 1

    # If today has 0 contributions yet, check if yesterday was part of an active streak
    if idx >= 0 and sorted_days[idx]["count"] == 0:
        if idx - 1 >= 0 and sorted_days[idx - 1]["count"] > 0:
            idx -= 1

    while idx >= 0 and sorted_days[idx]["count"] > 0:
        current_streak += 1
        idx -= 1

    return current_streak, longest_streak


def fetch_contributions(username: str = USERNAME) -> dict:
    """Scrape GitHub contribution graph and extract daily counts and streak stats."""
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": USER_AGENT}

    print(f"[fetch_contributions] Fetching URL: {url}")
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print(f"Error: GitHub returned status code {response.status_code}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    # Map tool-tip elements by target ID
    tooltip_map = {}
    for tt in soup.find_all("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltip_map[for_id] = tt.get_text(strip=True)

    # Extract all calendar day table cells
    td_cells = soup.find_all("td", class_=lambda c: c and "ContributionCalendar-day" in c)
    if not td_cells:
        print("Warning: No ContributionCalendar-day cells found in HTML page.", file=sys.stderr)

    days_list = []
    total_contributions = 0

    for td in td_cells:
        date_str = td.get("data-date")
        if not date_str:
            continue

        level = int(td.get("data-level", 0))
        td_id = td.get("id", "")
        tt_text = tooltip_map.get(td_id, "")

        count = 0
        if tt_text and "No contributions" not in tt_text:
            match = re.search(r"(\d+)\s+contribution", tt_text)
            if match:
                count = int(match.group(1))
            elif level > 0:
                count = level  # Fallback estimate if string parsing fails
        elif "No contributions" in tt_text:
            count = 0

        days_list.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        total_contributions += count

    # Sort chronologically
    days_list.sort(key=lambda d: d["date"])

    current_streak, longest_streak = calculate_streaks(days_list)

    result_data = {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_days": len(days_list),
        "days": days_list
    }

    return result_data


def main() -> None:
    """Fetch contributions and save to data/contributions.json."""
    data = fetch_contributions(USERNAME)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[fetch_contributions] Successfully saved {len(data['days'])} days to {OUTPUT_JSON}")
    print(f"[fetch_contributions] Total: {data['total_contributions']} | Current Streak: {data['current_streak']} | Longest Streak: {data['longest_streak']}")


if __name__ == "__main__":
    main()
