import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://www.espn.com/nhl/teams"
OUTPUT_FILE = "data/hockey/teams/hockey_NHL_teams.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}


def extract_team_id(href: str) -> str | None:
    parts = href.strip("/").split("/")
    if "name" in parts:
        return parts[parts.index("name") + 1]
    return None


def scrape_nhl_teams():
    response = requests.get(URL, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    teams = []

    for section in soup.select("section.TeamLinks"):
        link = section.find("a", href=True)
        img = section.find("img")
        name_tag = section.find("h2")

        if not (link and img and name_tag):
            continue

        team_id = extract_team_id(link["href"])
        if not team_id:
            continue

        teams.append({
            "team": name_tag.text.strip(),
            "team_id": team_id,
            "logo": urljoin("https://www.espn.com", img["src"])
        })

    data = {
        "NHL": teams
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(teams)} équipes NHL sauvegardées")


if __name__ == "__main__":
    scrape_nhl_teams()