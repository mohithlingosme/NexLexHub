"use client";

import { FormEvent, useState } from "react";

import { apiBase, apiKey } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type SearchResult = {
  case_id: number;
  title: string;
  citation: string | null;
  text: string;
  score: number;
  verified: boolean;
};

export default function SearchPage() {
  const [query, setQuery] = useState("Cases where investigation cannot be quashed at threshold");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${apiBase}/semantic-search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": apiKey,
        },
        body: JSON.stringify({ query, limit: 8 }),
      });
      const payload = (await response.json()) as { results?: SearchResult[] };
      setResults(payload.results ?? []);
    } finally {
      setLoading(false);
    }
  }

  return (
    <WorkspaceShell title="Semantic Search" eyebrow="Natural Language Retrieval">
      <div className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
        <Panel title="Search console" subtitle="Hybrid retrieval over citation-aware judgment chunks.">
          <form onSubmit={onSubmit} className="space-y-4">
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="min-h-32 w-full rounded-2xl border border-white/10 bg-shell px-4 py-4 text-sm text-white outline-none"
            />
            <button className="rounded-2xl bg-accent px-5 py-3 text-sm font-medium text-white">
              {loading ? "Retrieving..." : "Run semantic retrieval"}
            </button>
          </form>
        </Panel>
        <Panel title="Filters" subtitle="Placeholder for court, date, treatment, and statute facets.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Court: Supreme Court, High Courts, Tribunals</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Treatment: relied upon, distinguished, overruled</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Grounding: official-source only</div>
          </div>
        </Panel>
      </div>
      <div className="mt-5">
        <Panel title="Results" subtitle="Each result keeps citation and verification state visible.">
          <div className="space-y-4">
            {results.map((result) => (
              <article key={`${result.case_id}-${result.score}`} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex flex-wrap items-center gap-3">
                  <h4 className="text-base font-medium text-white">{result.title}</h4>
                  <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-shell-muted">
                    score {result.score}
                  </span>
                  <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
                    {result.verified ? "officially linked" : "publisher linked"}
                  </span>
                </div>
                <p className="mt-2 text-sm text-shell-muted">{result.citation}</p>
                <p className="mt-3 text-sm leading-7 text-slate-200">{result.text}</p>
              </article>
            ))}
            {!results.length && <p className="text-sm text-shell-muted">Run a query to view retrieved chunks.</p>}
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
