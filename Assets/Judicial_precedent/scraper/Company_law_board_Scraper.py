import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://indiankanoon.org"
start_url = "https://indiankanoon.org/browse/clb/"
BASE_DIR = "Company_Law_Board"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/pdf,application/xhtml+xml"
}

session = requests.Session()
session.headers.update(HEADERS)


# -----------------------------
# UTIL FUNCTIONS
# -----------------------------

def get_soup(url, params=None):
    try:
        res = session.get(url, params=params, timeout=15)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None


def clean_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name[:150]


# -----------------------------
# STEP 1: GET YEAR LINKS
# -----------------------------
def get_year_links():
    soup = get_soup(START_URL)
    links = []

    for a in soup.select(".browselist a"):
        href = a.get("href")
        if href:
            links.append(urljoin(BASE_URL, href))

    return links


# -----------------------------
# STEP 2: GET ENTIRE YEAR LINK
# -----------------------------
def get_entire_year_search(year_url):
    soup = get_soup(year_url)
    if not soup:
        return None

    for a in soup.find_all("a"):
        if "Entire Year" in a.text:
            return urljoin(BASE_URL, a.get("href"))

    return None


# -----------------------------
# STEP 3: GET CASE LINKS
# -----------------------------
def get_case_links(search_url):
    links = set()

    for page in range(0, 100):
        params = {"pagenum": page}
        soup = get_soup(search_url, params)

        if not soup:
            break

        results = soup.find_all("article", class_="result")

        if not results:
            print(f"⛔ End at page {page}")
            break

        count = 0

        for r in results:
            full_doc = r.find("a", string="Full Document")

            if full_doc:
                href = full_doc.get("href")
                if "/doc/" in href:
                    links.add(urljoin(BASE_URL, href))
                    count += 1

        print(f"📄 Page {page}: {count} cases")
        time.sleep(1)

    return list(links)


# -----------------------------
# STEP 4: GET CASE TITLE
# -----------------------------
def get_case_title(soup):
    try:
        return soup.find("h2", class_="doc_title").text.strip()
    except:
        return "case"


# -----------------------------
# STEP 5: DOWNLOAD PDF (FIXED)
# -----------------------------
def download_pdf(case_url, year, index):
    try:
        soup = get_soup(case_url)
        if not soup:
            return

        title = get_case_title(soup)
        filename = clean_filename(title) or f"case_{index}"

        year_folder = os.path.join(BASE_DIR, str(year))
        os.makedirs(year_folder, exist_ok=True)

        save_path = os.path.join(year_folder, f"{filename}.pdf")

        if os.path.exists(save_path):
            print("⏩ Exists:", filename)
            return

        doc_id = case_url.strip("/").split("/")[-1]
        post_url = f"{BASE_URL}/doc/{doc_id}/"

        # -----------------------------
        # STEP 1: POST REQUEST
        # -----------------------------
        response = session.post(
            post_url,
            data={"type": "pdf"},
            headers={
                "Referer": case_url,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=20
        )

        if "application/pdf" in response.headers.get("Content-Type", ""):
            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Saved (POST): {filename}")
            return

        # -----------------------------
        # STEP 2: FALLBACK GET
        # -----------------------------
        fallback_url = f"{BASE_URL}/doc/{doc_id}/?type=pdf"

        response = session.get(
            fallback_url,
            headers={"Referer": case_url},
            timeout=20
        )

        if "application/pdf" in response.headers.get("Content-Type", ""):
            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Saved (GET): {filename}")
        else:
            print("❌ Failed:", case_url)

        time.sleep(1)

    except Exception as e:
        print("❌ Error:", e)


# -----------------------------
# MAIN
# -----------------------------
def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    years = get_year_links()

    print(f"🚀 Found {len(years)} years")

    for year_url in years:
        year = year_url.strip("/").split("/")[-1]
        print(f"\n📅 YEAR: {year}")

        search_url = get_entire_year_search(year_url)

        if not search_url:
            print("❌ No 'Entire Year'")
            continue

        case_links = get_case_links(search_url)

        print(f"🔗 TOTAL CASES: {len(case_links)}")

        for i, case in enumerate(case_links):
            download_pdf(case, year, i)


if __name__ == "__main__":
    main()