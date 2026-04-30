Traceback (most recent call last):
  File "C:\Users\mohit\Documents\GitHub\NexLexHub\Pharse_1\Scraper\BarandBentch\Court_news\Sc.py", line 255, in <module>
    asyncio.run(scrape())
  File "C:\Users\mohit\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\mohit\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mohit\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\mohit\Documents\GitHub\NexLexHub\Pharse_1\Scraper\BarandBentch\Court_news\Sc.py", line 209, in scrape
    for category in CATEGORY_URLS:
                    ^^^^^^^^^^^^^
NameError: name 'CATEGORY_URLS' is not defined