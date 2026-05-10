"use client";

import { useEffect, useState } from "react";

import { apiBase, apiKey } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type CaseItem = {
  id: number;
  title: string;
  citation: string | null;
  decision_date: string | null;
  official_source_found: boolean;
};

export default function CasesPage() {
  const [cases, setCases] = useState<CaseItem[]>([]);

  useEffect(() => {
    fetch(`${apiBase}/cases`, { headers: { "X-API-Key": apiKey } })
      .then((response) => response.json())
      .then((payload) => setCases(payload as CaseItem[]))
      .catch(() => setCases([]));
  }, []);

  const selected = cases[0];

  return (
    <WorkspaceShell title="Case Explorer" eyebrow="Metadata + Holdings + Related Authorities">
      <div className="grid gap-5 xl:grid-cols-[260px_minmax(0,1fr)_320px]">
        <Panel title="Filters" subtitle="Court, date, issue cluster, and source fidelity.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Official source available</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Issue cluster: insolvency, transport</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Bench analytics and timeline pivots</div>
          </div>
        </Panel>
        <Panel title={selected?.title ?? "Judgment content"} subtitle={selected?.citation ?? "Select a case"}>
          <div className="space-y-4 text-sm leading-7 text-slate-200">
            {cases.map((item) => (
              <article key={item.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex flex-wrap items-center gap-3">
                  <h4 className="font-medium text-white">{item.title}</h4>
                  <span className="text-shell-muted">{item.decision_date}</span>
                </div>
                <p className="mt-2 text-shell-muted">{item.citation}</p>
                <p className="mt-3 text-shell-muted">
                  Workspace view for holdings, issues, statutes, and PDF-linked paragraph references.
                </p>
              </article>
            ))}
          </div>
        </Panel>
        <Panel title="Related graph" subtitle="Precedents, citation treatments, and linked authorities.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Relied upon edges</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Distinguished cases</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Statute references</div>
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
