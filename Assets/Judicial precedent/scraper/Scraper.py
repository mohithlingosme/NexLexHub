import requests
from bs4 import BeautifulSoup
import os
import time
import random

BASE = "https://indiankanoon.org"
HEADERS = {"User-Agent": "Mozilla/5.0"}

START_YEAR = 1949
END_YEAR = 2026

SLEEP_MIN = 2
SLEEP_MAX = 4


COURTS = {
    "karnataka_high_court": "Karnataka High Court",
    "madras_high_court": "Madras High Court",
    "delhi_high_court": "Delhi High Court",
    "bombay_high_court": "Bombay High Court",
    "calcutta_high_court": "Calcutta High Court"
}


def create_path(court, year):
    base = "Judicial Precedent/High Courts"
    path = f"{base}/{court}/{year}"
    os.makedirs(path, exist_ok=True)
    return path


def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-")[:120]


def safe_get(session, url):
    for i in range(3):
        try:
            return session.get(url, headers=HEADERS, timeout=15)
        except:
            time.sleep(2)
    return None


def get_links(session, court_key, year, page):
    url = f"{BASE}/search/?formInput=doctypes:{court_key} year:{year}&pagenum={page}"

    print("🔍", url)

    res = safe_get(session, url)
    if not res:
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        if "/doc/" in a["href"]:
            links.append(BASE + a["href"])

    return list(set(links))


def download_pdf(session, url):
    res = safe_get(session, url)
    if not res:
        return None, None, None

    soup = BeautifulSoup(res.text, "html.parser")

    token = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if not token:
        return None, None, None

    csrf = token["value"]

    try:
        title = soup.find("h2", class_="doc_title").text.strip()
    except:
        title = "case"

    try:
        court = soup.find("h3", class_="docsource_main").text.strip()
    except:
        court = "Unknown Court"

    try:
        pdf_res = session.post(
            url,
            data={
                "type": "pdf",
                "csrfmiddlewaretoken": csrf
            },
            headers={**HEADERS, "Referer": url},
            timeout=20
        )
    except:
        return None, None, None

    if "application/pdf" not in pdf_res.headers.get("Content-Type", ""):
        return None, None, None

    return title, court, pdf_res.content


def main():
    session = requests.Session()

    total = 0

    for court_key, court_name in COURTS.items():
        print(f"\n🏛️ {court_name}")

        for year in range(START_YEAR, END_YEAR + 1):
            print(f"\n📅 {year}")

            empty_pages = 0

            for page in range(0, 100):
                print(f"📄 Page {page}")

                links = get_links(session, court_key, year, page)

                if not links:
                    empty_pages += 1
                    if empty_pages >= 3:
                        break
                    continue

                empty_pages = 0

                for link in links:
                    try:
                        title, court, pdf = download_pdf(session, link)

                        if not pdf:
                            continue

                        folder = create_path(court_name, year)

                        filename = clean_filename(title) + ".pdf"
                        filepath = os.path.join(folder, filename)

                        if os.path.exists(filepath):
                            continue

                        with open(filepath, "wb") as f:
                            f.write(pdf)

                        total += 1
                        print("✅", total, filename[:80])

                    except:
                        continue

                    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

    print("\n🎉 TOTAL:", total)


if __name__ == "__main__":
    main()