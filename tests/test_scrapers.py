from __future__ import annotations

from nexlexhub.scrapers.discovery import (
    BarAndBenchAllahabadHighCourtEngine,
    BarAndBenchSupremeCourtEngine,
    LiveLawKarnatakaHighCourtEngine,
    LiveLawSupremeCourtEngine,
)


def test_scraper_configuration() -> None:
    engines = [
        LiveLawSupremeCourtEngine(),
        BarAndBenchSupremeCourtEngine(),
        LiveLawKarnatakaHighCourtEngine(),
        BarAndBenchAllahabadHighCourtEngine(),
    ]
    assert all(engine.publisher and engine.topic_urls and engine.court for engine in engines)
