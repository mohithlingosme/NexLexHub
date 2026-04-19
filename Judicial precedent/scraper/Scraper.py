import requests
from bs4 import BeautifulSoup
import os
import time

BASE = "https://indiankanoon.org"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SLEEP = 2


# =========================
# CREATE FOLDER
# =========================
def create_path(court, year):
    base = "Judicial Precedent"

    if "Supreme Court" in court:
        path = f"{base}/Supreme Court/{year}"
    elif "Privy" in court:
        path = f"{base}/Privy Council/{year}"
    else:
        path = f"{base}/High Courts/{court}/{year}"

    os.makedirs(path, exist_ok=True)
    return path


# =========================
# GET PDF
# =========================
def download_pdf(session, url):
    res = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # Extract CSRF token
    token = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if not token:
        return None, None, None

    csrf = token["value"]

    # Extract metadata
    try:
        title = soup.find("h2", class_="doc_title").text.strip()
    except:
        title = "case"

    try:
        court = soup.find("h3", class_="docsource_main").text.strip()
    except:
        court = "Unknown Court"

    # POST request to get PDF
    pdf_res = session.post(
        url,
        data={
            "type": "pdf",
            "csrfmiddlewaretoken": csrf
        },
        headers={
            **HEADERS,
            "Referer": url
        }
    )

    if "application/pdf" not in pdf_res.headers.get("Content-Type", ""):
        return None, None, None

    return title, court, pdf_res.content


# =========================
# CLEAN FILE NAME
# =========================
def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-")[:100]


# =========================
# GET CASE LINKS
# =========================
def get_links(year, page):
    url = f"{BASE}/search/?formInput=doctypes:karnataka year:{year}&pagenum={page}"

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        if "/doc/" in a["href"]:
            links.append(BASE + a["href"])

    return list(set(links))


# =========================
# MAIN
# =========================
def main():
    session = requests.Session()

    year = 1949

    for page in range(0, 3):  # limit
        print(f"\n📄 Page {page}")

        links = get_links(year, page)

        if not links:
            break

        for link in links:
            try:
                title, court, pdf = download_pdf(session, link)

                if not pdf:
                    print("❌ PDF failed")
                    continue

                folder = create_path(court, year)

                filename = clean_filename(title) + ".pdf"
                filepath = os.path.join(folder, filename)

                if os.path.exists(filepath):
                    continue

                with open(filepath, "wb") as f:
                    f.write(pdf)

                print("✅ Saved:", filename)

            except Exception as e:
                print("❌ Error:", e)

            time.sleep(SLEEP)


if __name__ == "__main__":
    main()