#!/usr/bin/env python3
"""
scripts/fetch_codeforces.py

Fetches official Codeforces stats using public Codeforces REST APIs.
Saves extracted metrics to data/codeforces.json.
"""

import json
import sys
from datetime import datetime, timezone
import requests
from config import CODEFORCES_JSON, CODEFORCES_USERNAME, DATA_DIR

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def fetch_codeforces_data(handle: str = CODEFORCES_USERNAME) -> dict:
    """Fetch user info, contest rating history, and problem submission stats from official Codeforces API."""
    headers = {"User-Agent": USER_AGENT}
    print(f"[fetch_codeforces] Fetching data for handle: '{handle}'...")

    result = {
        "handle": handle,
        "rating": 0,
        "max_rating": 0,
        "rank": "Unranked",
        "max_rank": "Unranked",
        "contests": 0,
        "problems_solved": 0,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "OK",
    }

    # 1. Fetch User Info
    info_url = f"https://codeforces.com/api/user.info?handles={handle}"
    try:
        r_info = requests.get(info_url, headers=headers, timeout=12)
        if r_info.status_code == 200:
            data = r_info.json()
            if data.get("status") == "OK" and data.get("result"):
                user = data["result"][0]
                result["rating"] = user.get("rating", 0)
                result["max_rating"] = user.get("maxRating", 0)
                result["rank"] = user.get("rank", "Unranked").title()
                result["max_rank"] = user.get("maxRank", "Unranked").title()
    except Exception as e:
        print(f"[fetch_codeforces] Warning: Failed to fetch user info: {e}", file=sys.stderr)

    # 2. Fetch Rating History (Contest Count)
    rating_url = f"https://codeforces.com/api/user.rating?handle={handle}"
    try:
        r_rating = requests.get(rating_url, headers=headers, timeout=12)
        if r_rating.status_code == 200:
            data = r_rating.json()
            if data.get("status") == "OK":
                result["contests"] = len(data.get("result", []))
    except Exception as e:
        print(f"[fetch_codeforces] Warning: Failed to fetch rating history: {e}", file=sys.stderr)

    # 3. Fetch Submissions (Problems Solved)
    status_url = f"https://codeforces.com/api/user.status?handle={handle}"
    try:
        r_status = requests.get(status_url, headers=headers, timeout=15)
        if r_status.status_code == 200:
            data = r_status.json()
            if data.get("status") == "OK":
                solved_set = set()
                for sub in data.get("result", []):
                    if sub.get("verdict") == "OK" and "problem" in sub:
                        prob = sub["problem"]
                        # Unique identifier using contestId + index or name
                        prob_id = f"{prob.get('contestId', '')}_{prob.get('index', '')}_{prob.get('name', '')}"
                        solved_set.add(prob_id)
                result["problems_solved"] = len(solved_set)
    except Exception as e:
        print(f"[fetch_codeforces] Warning: Failed to fetch submissions: {e}", file=sys.stderr)

    return result


def main() -> None:
    """Main execution entry point."""
    data = fetch_codeforces_data(CODEFORCES_USERNAME)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CODEFORCES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[fetch_codeforces] Successfully saved metrics to {CODEFORCES_JSON}")
    print(f"[fetch_codeforces] Handle: {data['handle']} | Rating: {data['rating']} (Max: {data['max_rating']}) | Rank: {data['rank']} | Solved: {data['problems_solved']} | Contests: {data['contests']}")


if __name__ == "__main__":
    main()
