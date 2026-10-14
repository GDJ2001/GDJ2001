"""Refresh a private-activity grade locally without publishing private counts.

Requires the repository owner's authenticated GitHub CLI session. This script is
intentionally not part of GitHub Actions: the workflow token cannot read the
owner's private contribution history.
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "GDJ2001"
QUERY = "{ viewer { login contributionsCollection { restrictedContributionsCount } } }"


def grade_for(count):
    """Custom contribution-volume tier over the owner's last 12 months."""
    if count >= 5000:
        return "S"
    if count >= 3000:
        return "A+"
    if count >= 2000:
        return "A"
    if count >= 1000:
        return "B+"
    if count >= 250:
        return "B"
    return "C"


def render(grade, date, mobile=False):
    if mobile:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="260" viewBox="0 0 480 260" role="img" aria-labelledby="title">
  <title id="title">Private activity grade {grade}, custom contribution volume tier, verified {date} UTC</title>
  <defs><linearGradient id="accent"><stop stop-color="#58e8d4"/><stop offset="1" stop-color="#74a7ff"/></linearGradient></defs>
  <rect width="480" height="260" rx="16" fill="#0b1627"/>
  <rect x=".5" y=".5" width="479" height="259" rx="16" fill="none" stroke="#263a54"/>
  <g font-family="Segoe UI,Arial,sans-serif" text-anchor="middle">
    <text x="240" y="37" font-size="13" letter-spacing="2" fill="#b5c6d8">PRIVATE ACTIVITY GRADE</text>
    <text x="240" y="146" font-size="100" font-weight="700" fill="url(#accent)">{grade}</text>
    <text x="240" y="188" font-size="18" fill="#e6edf3">Owner-verified contribution tier</text>
    <text x="240" y="218" font-size="13" fill="#8da9c0">No private repo details shared</text>
    <text x="240" y="244" font-size="11" fill="#8da9c0">VERIFIED {date.upper()} UTC</text>
  </g>
</svg>\n'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="228" viewBox="0 0 960 228" role="img" aria-labelledby="title">
  <title id="title">Private activity grade {grade}, custom contribution volume tier, verified {date} UTC</title>
  <defs><linearGradient id="accent"><stop stop-color="#58e8d4"/><stop offset="1" stop-color="#74a7ff"/></linearGradient></defs>
  <rect width="960" height="228" rx="16" fill="#0b1627"/>
  <rect x=".5" y=".5" width="959" height="227" rx="16" fill="none" stroke="#263a54"/>
  <path d="M675 28V185" stroke="#263a54"/>
  <g font-family="Segoe UI,Arial,sans-serif">
    <text x="40" y="50" font-size="14" letter-spacing="2" fill="#58e8d4">PRIVATE ACTIVITY GRADE</text>
    <text x="40" y="98" font-size="31" font-weight="700" fill="#e6edf3">Work beyond the public repos.</text>
    <text x="40" y="131" font-size="18" fill="#b5c6d8">A custom contribution-volume tier,</text>
    <text x="40" y="158" font-size="18" fill="#b5c6d8">verified with owner-visible GitHub activity.</text>
    <text x="40" y="201" font-size="12" fill="#8da9c0">NO PRIVATE REPOSITORY DETAILS SHARED · VERIFIED {date.upper()} UTC</text>
    <text x="817" y="154" text-anchor="middle" font-size="118" font-weight="700" fill="url(#accent)">{grade}</text>
    <text x="817" y="188" text-anchor="middle" font-size="13" fill="#b5c6d8">CONTRIBUTION TIER</text>
  </g>
</svg>\n'''


def main():
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    viewer = json.loads(result.stdout)["data"]["viewer"]
    if viewer["login"].casefold() != USERNAME.casefold():
        raise ValueError("Authenticated GitHub account does not own this profile.")
    count = viewer["contributionsCollection"]["restrictedContributionsCount"]
    grade = grade_for(count)
    date = datetime.now(timezone.utc).strftime("%d %b %Y")
    for mobile in (False, True):
        name = "private-grade-mobile.svg" if mobile else "private-grade.svg"
        (ROOT / "assets" / name).write_text(render(grade, date, mobile), encoding="utf-8")
    print(f"Updated private activity grade: {grade}. No private counts or repository data written.")


if __name__ == "__main__":
    main()
