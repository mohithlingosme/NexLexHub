# Deduplication Refactor Plan for ScArticles_Redudancy_Remove.py

Current Progress: 12/12 steps complete ✅

## Steps:
1. [ ] Update config: Use relative paths, dataclass for settings
2. [ ] Improve normalize_title: Better punctuation handling
3. [ ] Add robust date parsing (dateutil)
4. [ ] Implement fuzzy content dedup (jellyfish)
5. [ ] Use LRU cache for title similarity
6. [ ] Enhance SC filtering (expand keywords)
7. [ ] Add input validation/JSON schema check
8. [ ] Add CLI args (argparse)
9. [ ] Integrate progress bar (tqdm)
10. [ ] Add error handling/logging
11. [ ] Create unit tests (test_dedupe.py)
12. [ ] Benchmark and document

## Testing:
- [ ] Run on full dataset
- [ ] Verify no regressions in duplicates
- [ ] Check memory/performance

Next: Install deps then step 1 edits.
