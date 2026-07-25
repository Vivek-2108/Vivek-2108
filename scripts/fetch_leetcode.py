#!/usr/bin/env python3
"""
scripts/fetch_leetcode.py

Fetches public LeetCode stats including solved problem breakdown (Easy/Medium/Hard),
ranking, contest rating, and acceptance rate.
Saves metrics to data/leetcode.json.
"""

import json
import sys
from datetime import datetime, timezone
import requests
from config import LEETCODE_JSON, LEETCODE_USERNAME, DATA_DIR

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def fetch_leetcode_data(username: str = LEETCODE_USERNAME) -> dict:
    """Fetch profile metrics and contest data from public LeetCode REST services."""
    headers = {"User-Agent": USER_AGENT}
    print(f"[fetch_leetcode] Fetching data for username: '{username}'...")

    result = {
        "username": username,
        "total_solved": 0,
        "easy_solved": 0,
        "medium_solved": 0,
        "hard_solved": 0,
        "ranking": 0,
        "acceptance_rate": 0.0,
        "contest_rating": 0,
        "contest_ranking": 0,
        "contests_attended": 0,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "OK",
    }

    # 1. Fetch General User Profile & Solved Breakdown
    profile_url = f"https://alfa-leetcode-api.onrender.com/userProfile/{username}"
    try:
        r_prof = requests.get(profile_url, headers=headers, timeout=12)
        if r_prof.status_code == 200:
            p_data = r_prof.json()
            result["total_solved"] = p_data.get("totalSolved", 0)
            result["easy_solved"] = p_data.get("easySolved", 0)
            result["medium_solved"] = p_data.get("mediumSolved", 0)
            result["hard_solved"] = p_data.get("hardSolved", 0)
            result["ranking"] = p_data.get("ranking", 0)

            # Calculate Acceptance Rate
            sub_stats = p_data.get("totalSubmissions", [])
            ac_stats = p_data.get("matchedUserStats", {}).get("acSubmissionNum", [])
            
            total_subs = 0
            for item in sub_stats:
                if item.get("difficulty") == "All":
                    total_subs = item.get("submissions", 0)
                    break

            total_ac = 0
            for item in ac_stats:
                if item.get("difficulty") == "All":
                    total_ac = item.get("submissions", 0)
                    break

            if total_subs > 0:
                result["acceptance_rate"] = round((total_ac / total_subs) * 100, 1)

    except Exception as e:
        print(f"[fetch_leetcode] Warning: Failed to fetch profile info: {e}", file=sys.stderr)

    # 2. Fetch Contest Ranking & Rating Info
    contest_url = f"https://alfa-leetcode-api.onrender.com/userContestRankingInfo/{username}"
    try:
        r_contest = requests.get(contest_url, headers=headers, timeout=12)
        if r_contest.status_code == 200:
            c_data = r_contest.json()
            contest_user = c_data.get("userContestRanking", {})
            if contest_user:
                result["contest_rating"] = round(contest_user.get("rating", 0))
                result["contest_ranking"] = contest_user.get("globalRanking", 0)
                result["contests_attended"] = contest_user.get("attendedContestsCount", 0)
    except Exception as e:
        print(f"[fetch_leetcode] Warning: Failed to fetch contest info: {e}", file=sys.stderr)

    return result


def main() -> None:
    """Main execution entry point."""
    data = fetch_leetcode_data(LEETCODE_USERNAME)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LEETCODE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[fetch_leetcode] Successfully saved metrics to {LEETCODE_JSON}")
    print(f"[fetch_leetcode] Username: {data['username']} | Solved: {data['total_solved']} (E:{data['easy_solved']} M:{data['medium_solved']} H:{data['hard_solved']}) | Ranking: {data['ranking']} | Contest Rating: {data['contest_rating']} | Acc: {data['acceptance_rate']}%")


if __name__ == "__main__":
    main()
