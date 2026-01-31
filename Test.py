import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://www.espn.com/nhl/teams"
OUTPUT_FILE = "data/hockey/teams/hockey_NHL_teams.json"


def extract_team_id(href: str) -> str | None:
    """
    /nhl/team/_/name/bos/boston-bruins -> bos
    """
    parts = href.strip("/").split("/")
    if "name" in parts:
        return parts[parts.index("name") + 1]
    return None


def scrape_nhl_teams():
    response = requests.get(URL, timeout=15)
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

    print(f"✅ {len(teams)} équipes NHL sauvegardées dans {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_nhl_teams()