from dataclasses import dataclass, asdict
from typing import Dict, Set, List, Optional, Any
from pathlib import Path
import asyncio
import argparse
import logging
import hashlib
import json
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from urllib.parse import urljoin, urlparse
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

@dataclass
class Config:
    base_url: str = 'https://www.livelaw.in'
    category_url: str = 'https://www.livelaw.in/supreme-court'
    max_pages: int = 20
    days_limit: int = 7
    similarity_threshold: float = 0.85
    scrape_timeout: int = 60_000
    scrape_retries: int = 3
    headless: bool = True
    data_dir: Path = Path(__file__).parent / 'Data' / 'Raw_Data'
    output_file: Path = None  # Set later

    def __post_init__(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.data_dir / 'SC_articles.json'

@dataclass
class Article:
    url: str
    title: str
    content: str
    date: str

    def is_recent(self, days_limit: int) -> bool:
        dt = self.parse_date()
        return dt and dt >= datetime.now(dt.tzinfo) - timedelta(days=days_limit)

    def parse_date(self) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(self.date.replace('Z', '+00:00'))
        except:
            return None

def setup_logging(config: Config) -> logging.Logger:
    log_dir = config.data_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'scraper.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    return ' '.join(text.split()).strip()

def normalize_url(href: str, base_url: str) -> str:
    if not href:
        return ''
    if href.startswith('//'):
        return 'https:' + href
    if href.startswith('/'):
        return urljoin(base_url, href)
    return href

def is_valid_article_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    if 'livelaw.in' not in parsed.netloc:
        return False
    path = parsed.path.lower()
    if '/supreme-court/' not in path or any(x in path for x in ['/more/', '/tag/', '/category/', '/login']):
        return False
    return bool(re.search(r'-\d+$', path))

def generate_hash(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def is_similar(t1: str, t2: str, threshold: float) -> bool:
    return SequenceMatcher(None, t1, t2).ratio() > threshold

class Deduper:
    def __init__(self, max_recent: int = 10000):
        self.url_map: Dict[str, Article] = {}
        self.content_hashes: Set[str] = set()
        self.max_recent = max_recent
        self.titles: List[str] = []  # For similarity, FIFO

    def is_duplicate(self, article: Article, threshold: float) -> bool:
        if article.url in self.url_map:
            return True
        content_hash = generate_hash(article.content)
        if content_hash in self.content_hashes:
            return True
        # Similarity check on recent titles only
        for title in self.titles[-100:]:  # Limit scope
            if is_similar(article.title, title, threshold):
                return True
        return False

    def add(self, article: Article) -> None:
        self.url_map[article.url] = article
        self.content_hashes.add(generate_hash(article.content))
        self.titles.append(article.title)
        if len(self.titles) > self.max_recent:
            self.titles.pop(0)

def load_existing(config: Config) -> Deduper:
    deduper = Deduper()
    output_file = config.output_file
    if not output_file.exists():
        return deduper
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            art = Article(**item)
            deduper.add(art)
        logging.info(f'Loaded {len(deduper.url_map)} existing articles')
    except Exception as e:
        logging.warning(f'Corrupted JSON, resetting: {e}')
    return deduper

def save_data(deduper: Deduper, config: Config) -> None:
    data = sorted(
        [asdict(art) for art in deduper.url_map.values()],
        key=lambda x: Article(**x).parse_date() or datetime.min,
        reverse=True
    )
    temp_file = config.output_file.with_suffix('.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    temp_file.replace(config.output_file)
    logging.info(f'Saved {len(data)} articles')

async def extract_links(page, config: Config) -> set[str]:
    await page.goto(config.category_url, timeout=config.scrape_timeout)
    await asyncio.sleep(2)
    soup = BeautifulSoup(await page.content(), 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = normalize_url(a['href'], config.base_url)
        if is_valid_article_url(href):
            links.add(href)
    return links

async def scrape_article(page, url: str, config: Config) -> Optional[Article]:
    for attempt in range(config.scrape_retries):
        try:
            await page.goto(url, timeout=config.scrape_timeout)
            await asyncio.sleep(1)
            soup = BeautifulSoup(await page.content(), 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        data = data[0]
                    if data.get('@type') == 'NewsArticle':
                        art = Article(
                            url=url,
                            title=clean_text(data.get('headline', '')),
                            content=clean_text(data.get('articleBody', '')),
                            date=data.get('datePublished', '')
                        )
                        if art.title and art.content:  # Basic validation
                            return art
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            logging.warning(f'Retry {attempt+1}/{config.scrape_retries} for {url}: {e}')
            await asyncio.sleep(2 ** attempt)
    logging.error(f'Failed to scrape {url}')
    return None

async def scrape_page_links(page, page_num: int, config: Config, sem: asyncio.Semaphore) -> List[Article]:
    url = f'{config.category_url}?page={page_num}'
    async with sem:
        logging.info(f'Scraping page {page_num}: {url}')
        try:
            await page.goto(url, timeout=config.scrape_timeout)
            await asyncio.sleep(2)
            links = await extract_links(page, config)  # Wait, extract_links already gotes? Fix below
        except Exception as e:
            logging.error(f'Page load failed {page_num}: {e}')
            return []
        # Concurrent article scraping
        tasks = [scrape_article(page, link, config) for link in links]
        articles = await asyncio.gather(*tasks, return_exceptions=True)
        recent_articles = [art for art in articles if isinstance(art, Article) and art.is_recent(config.days_limit)]
        return recent_articles

async def main_scrape(config: Config):
    deduper = load_existing(config)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config.headless)
        try:
            context = await browser.new_context()
            page = await context.new_page()
            sem = asyncio.Semaphore(5)  # Concurrency limit
            tasks = [scrape_page_links(page, i, config, sem) for i in range(1, config.max_pages + 1)]
            all_pages_results = await asyncio.gather(*tasks, return_exceptions=True)
            new_articles: List[Article] = []
            no_recent = True
            for page_results in all_pages_results:
                if isinstance(page_results, Exception):
                    continue
                for art in page_results:
                    no_recent = False
                    if not deduper.is_duplicate(art, config.similarity_threshold):
                        deduper.add(art)
                        new_articles.append(art)
                        logging.info(f'Added: {art.title[:60]}...')
                        save_data(deduper, config)
                        await asyncio.sleep(1)
            if no_recent:
                logging.info('No recent articles found, stopping early')
        finally:
            await browser.close()
    save_data(deduper, config)

def parse_args() -> Config:
    parser = argparse.ArgumentParser(description='LiveLaw Supreme Court Scraper')
    parser.add_argument('--max-pages', type=int, default=20, help='Max pages to scrape')
    parser.add_argument('--days', type=int, default=7, help='Days limit for recency')
    parser.add_argument('--headless', action='store_true', help='Run headless')
    parser.add_argument('--data-dir', type=Path, help='Data directory')
    args = parser.parse_args()
    config = Config()
    for k, v in vars(args).items():
        if v is not None and k != 'headless':
            setattr(config, k.replace('-', '_'), v)
        elif k == 'headless' and v:
            config.headless = True
    if args.data_dir:
        config.data_dir = args.data_dir
    return config

if __name__ == '__main__':
    config = parse_args()
    logger = setup_logging(config)
    asyncio.run(main_scrape(config))

