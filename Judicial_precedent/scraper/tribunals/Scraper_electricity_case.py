import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://indiankanoon.org"
START_URL = "https://indiankanoon.org/browse/cegat/"
ROOT_DIR = "cegat"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
session.headers.update(HEADERS)


# ---------------------------
# UTIL
# ---------------------------
def clean_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()[:150]


def get_soup(url):
    try:
        res = session.get(url, timeout=15)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None


# ---------------------------
# STEP 1: YEARS
# ---------------------------
def get_years():
    soup = get_soup(START_URL)
    years = []

    if not soup:
        return years

    for a in soup.select(".browselist a"):
        year = a.text.strip()
        if year.isdigit():
            years.append((year, urljoin(BASE_URL, a["href"])))

    return years


# ---------------------------
# STEP 2: ENTIRE YEAR LINK
# ---------------------------
def get_entire_year_link(year_url):
    soup = get_soup(year_url)

    if not soup:
        print("❌ Failed year page:", year_url)
        return None

    a = soup.find("a", string=lambda x: x and "Entire Year" in x)

    if not a:
        print("❌ No 'Entire Year':", year_url)
        return None

    return urljoin(BASE_URL, a["href"])


# ---------------------------
# STEP 3: CASE LINKS
# ---------------------------
def get_case_links(search_url):
    cases = []

    page = 1

    while True:
        url = search_url if page == 1 else f"{search_url}&pagenum={page-1}"
        print(f"📄 Page {page}")

        soup = get_soup(url)
        if not soup:
            break

        results = soup.select("article.result")

        if not results:
            print("⛔ End")
            break

        for r in results:
            doc = r.select_one('a[href^="/doc/"]')
            if doc:
                cases.append(urljoin(BASE_URL, doc["href"]))

        page += 1
        time.sleep(1)

    return list(set(cases))


# ---------------------------
# STEP 4: DOWNLOAD PDF
# ---------------------------
def download_pdf(case_url, year):
    try:
        # STEP 1: GET PAGE (same session)
        res = session.get(case_url, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # TITLE
        title_tag = soup.select_one(".doc_title")
        title = title_tag.text.strip() if title_tag else "case"

        filename = clean_filename(title)

        # CREATE FOLDER
        folder = os.path.join(ROOT_DIR, year)
        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, f"{filename}.pdf")

        if os.path.exists(file_path):
            print("⏭️ Exists:", filename)
            return

        # CHECK PDF BUTTON
        pdf_button = soup.find("button", id="pdfdoc")
        if not pdf_button:
            print("⛔ No PDF:", case_url)
            return

        form = pdf_button.find_parent("form")

        csrf = form.find("input", {"name": "csrfmiddlewaretoken"})
        csrf_token = csrf["value"] if csrf else ""

        doc_id = case_url.strip("/").split("/")[-1]

        # STEP 2: POST (IMPORTANT)
        pdf_res = session.post(
            f"{BASE_URL}/doc/{doc_id}/",
            data={
                "type": "pdf",
                "csrfmiddlewaretoken": csrf_token
            },
            headers={"Referer": case_url},
            timeout=20
        )

        # FALLBACK
        if "application/pdf" not in pdf_res.headers.get("Content-Type", ""):
            pdf_res = session.get(
                f"{BASE_URL}/doc/{doc_id}/?type=pdf",
                headers={"Referer": case_url},
                timeout=20
            )

        # FINAL CHECK
        if "application/pdf" in pdf_res.headers.get("Content-Type", ""):
            with open(file_path, "wb") as f:
                f.write(pdf_res.content)

            print("✅ Saved:", filename)
        else:
            print("❌ Failed PDF:", case_url)

        time.sleep(1)

    except Exception as e:
        print("❌ Error:", e)


# ---------------------------
# MAIN
# ---------------------------
def main():
    os.makedirs(ROOT_DIR, exist_ok=True)

    years = get_years()
    print(f"📊 Years found: {len(years)}")

    for year, year_url in years:
        print(f"\n📅 YEAR: {year}")

        search_url = get_entire_year_link(year_url)
        if not search_url:
            continue

        cases = get_case_links(search_url)
        print(f"🔗 Total cases: {len(cases)}")

        for i, case in enumerate(cases):
            print(f"➡️ {i+1}/{len(cases)}")
            download_pdf(case, year)


if __name__ == "__main__":
    main()