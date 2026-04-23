import os
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

BASE_URL = "https://indiankanoon.org"
START_URL = "https://indiankanoon.org/browse/karnataka/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OUTPUT_DIR = "karnataka_cases"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_soup(url):
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None


# Step 1: Get all year links
def get_year_links():
    soup = get_soup(START_URL)
    links = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "/browse/karnataka/" in href and href.count("/") == 4:
            links.append(BASE_URL + href)

    return list(set(links))


# Step 2: Get "Entire Year" link
def get_entire_year_link(year_url):
    soup = get_soup(year_url)
    if not soup:
        return None

    for a in soup.find_all("a"):
        if "Entire Year" in a.text:
            return BASE_URL + a.get("href")

    return None


# Step 3: Extract case links
def get_case_links(entire_url):
    soup = get_soup(entire_url)
    if not soup:
        return []

    links = []
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "/doc/" in href:
            links.append(BASE_URL + href)

    return list(set(links))


# Step 4: Extract case content
def scrape_case(url):
    soup = get_soup(url)
    if not soup:
        return None

    try:
        title = soup.find("title").text.strip()

        content_div = soup.find("div", {"class": "judgments"})
        text = content_div.get_text(separator="\n") if content_div else ""

        return {
            "url": url,
            "title": title,
            "content": text
        }
    except:
        return None


# Step 5: Save case
def save_case(year, index, data):
    year_dir = os.path.join(OUTPUT_DIR, year)
    os.makedirs(year_dir, exist_ok=True)

    filename = os.path.join(year_dir, f"case_{index}.json")

    if os.path.exists(filename):
        return  # idempotent

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# MAIN PIPELINE
def main():
    years = get_year_links()

    print(f"Found {len(years)} years")

    for year_url in years:
        year = year_url.strip("/").split("/")[-1]
        print(f"\n📅 Processing Year: {year}")

        entire_link = get_entire_year_link(year_url)
        if not entire_link:
            continue

        case_links = get_case_links(entire_link)
        print(f"🔗 Found {len(case_links)} cases")

        for i, case_url in enumerate(tqdm(case_links)):
            data = scrape_case(case_url)

            if data:
                save_case(year, i, data)

            time.sleep(1)  # anti-block


if __name__ == "__main__":
    main()