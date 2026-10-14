"""Refresh the self-hosted profile card from public GitHub API data.

Run: python scripts/update_profile.py
Optional: GITHUB_TOKEN to increase the API rate limit. No third-party packages.
"""

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from profile_metrics import build_metrics

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "GDJ2001"


def github(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "GDJ2001-profile"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/{path}", headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def github_graphql(query, variables):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = subprocess.run(["gh", "auth", "token"], check=True, capture_output=True,
                               text=True, encoding="utf-8").stdout.strip()
    request = Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json",
                 "Authorization": f"Bearer {token}", "User-Agent": "GDJ2001-profile"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors") or not result.get("data", {}).get("user"):
        raise ValueError("GitHub did not return the public profile rank data.")
    return result["data"]["user"]


def main():
    user = github(f"users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = github(f"users/{USERNAME}/repos?type=owner&per_page=100&page={page}")
        repos.extend(repo for repo in batch if not repo.get("private", False))
        if len(batch) < 100:
            break
        page += 1

    # Complete every remote fetch before updating any committed assets.
    rank_query = """query($login: String!, $from: DateTime!) {
      user(login: $login) {
        followers { totalCount }
        commits: contributionsCollection(from: $from) { totalCommitContributions }
        reviews: contributionsCollection { totalPullRequestReviewContributions }
        pullRequests(first: 1) { totalCount }
        openedIssues: issues(states: OPEN) { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
      }
    }"""
    rank_data = github_graphql(rank_query, {
        "login": user["login"],
        "from": f"{datetime.now(timezone.utc).year}-01-01T00:00:00Z",
    })
    metric_artifacts = build_metrics(user, repos, github, rank_data)
    stats = [
        ("PUBLIC REPOSITORIES", len(repos)),
        ("FOLLOWERS", user["followers"]),
        ("STARS ON PUBLIC REPOS", sum(repo["stargazers_count"] for repo in repos)),
    ]
    date = datetime.now(timezone.utc).strftime("%d %b %Y")
    columns = []
    for index, (label, value) in enumerate(stats):
        x = 160 + index * 320
        columns.append(f'<text x="{x}" y="96" font-size="46" font-weight="700" fill="#58e8d4">{value}</text>'
                       f'<text x="{x}" y="128" font-size="12" letter-spacing="1.4" fill="#b5c6d8">{label}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="190" viewBox="0 0 960 190" role="img" aria-labelledby="title desc">
  <title id="title">GDJ2001 public GitHub overview</title>
  <desc id="desc">{'; '.join(f'{label}: {value}' for label, value in stats)}. Updated {date} UTC.</desc>
  <rect width="960" height="190" rx="16" fill="#0b1627"/>
  <rect x=".5" y=".5" width="959" height="189" rx="16" fill="none" stroke="#263a54"/>
  <path d="M320 48V138M640 48V138" stroke="#263a54"/>
  <g font-family="Segoe UI,Arial,sans-serif" text-anchor="middle">
    {''.join(columns)}
    <text x="480" y="169" font-size="11" fill="#8da9c0">PUBLIC GITHUB DATA · UPDATED {date.upper()} UTC</text>
  </g>
</svg>
'''
    # Fetch everything before writing, so API errors preserve the previous card.
    destination = ROOT / "assets" / "github-overview.svg"
    destination.parent.mkdir(exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(svg, encoding="utf-8")
    temporary.replace(destination)
    mobile_rows = []
    for index, (label, value) in enumerate(stats):
        y = 60 + index * 90
        mobile_rows.append(f'<text x="38" y="{y}" font-size="36" font-weight="700" fill="#58e8d4">{value}</text>'
                           f'<text x="138" y="{y - 7}" font-size="14" fill="#b5c6d8">{label}</text>')
    mobile = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320" viewBox="0 0 480 320" role="img" aria-labelledby="title">
  <title id="title">GDJ2001 public GitHub statistics, updated {date} UTC</title>
  <rect width="480" height="320" rx="16" fill="#0b1627"/>
  <rect x=".5" y=".5" width="479" height="319" rx="16" fill="none" stroke="#263a54"/>
  <path d="M30 90H450M30 180H450" stroke="#263a54"/>
  <g font-family="Segoe UI,Arial,sans-serif">{''.join(mobile_rows)}
    <text x="240" y="294" text-anchor="middle" font-size="12" fill="#8da9c0">UPDATED {date.upper()} UTC</text>
  </g>
</svg>
'''
    (ROOT / "assets" / "github-overview-mobile.svg").write_text(mobile, encoding="utf-8")
    for name, svg in metric_artifacts.items():
        (ROOT / "assets" / name).write_text(svg, encoding="utf-8")
    print(f"Updated public profile cards: {len(repos)} repositories, {user['followers']} followers.")


if __name__ == "__main__":
    main()
