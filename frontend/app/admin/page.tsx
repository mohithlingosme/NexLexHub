"use client";

import { useEffect, useState } from "react";

import { apiBase } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type Counts = {
  cases?: number;
  events?: number;
  statutes?: number;
  alerts?: number;
};

export default function AdminPage() {
  const [counts, setCounts] = useState<Counts>({});

  useEffect(() => {
    fetch(`${apiBase}/health`)
      .then((response) => response.json())
      .then((payload: { counts?: Counts }) => setCounts(payload.counts ?? {}))
      .catch(() => setCounts({}));
  }, []);

  return (
    <WorkspaceShell title="Admin Dashboard" eyebrow="System Health + Data Plane">
      <div className="grid gap-5 md:grid-cols-4">
        {Object.entries(counts).map(([key, value]) => (
          <Panel key={key} title={key} subtitle="Current dataset footprint">
            <div className="text-4xl font-semibold text-white">{value}</div>
          </Panel>
        ))}
      </div>
      <div className="mt-5">
        <Panel title="Operations" subtitle="Infrastructure and queue status surfaces belong here.">
          <div className="grid gap-4 md:grid-cols-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">PostgreSQL + pgvector</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Redis + Celery workers</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Official source ingestion health</div>
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
