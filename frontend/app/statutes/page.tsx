"use client";

import { useEffect, useState } from "react";

import { apiBase, apiKey } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type Statute = {
  id: number;
  name: string;
  citation: string | null;
  source_url: string | null;
};

export default function StatutesPage() {
  const [statutes, setStatutes] = useState<Statute[]>([]);

  useEffect(() => {
    fetch(`${apiBase}/statutes`, { headers: { "X-API-Key": apiKey } })
      .then((response) => response.json())
      .then((payload) => setStatutes(payload as Statute[]))
      .catch(() => setStatutes([]));
  }, []);

  return (
    <WorkspaceShell title="Statute Explorer" eyebrow="Acts, Sections, and Cross-References">
      <Panel title="Statute references" subtitle="Linked to judgment chunks and retrieval evidence.">
        <div className="grid gap-4 md:grid-cols-2">
          {statutes.map((statute) => (
            <article key={statute.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <h4 className="text-base font-medium text-white">{statute.name}</h4>
              <p className="mt-2 text-sm text-shell-muted">{statute.citation}</p>
              <p className="mt-2 break-all text-xs text-shell-muted">{statute.source_url}</p>
            </article>
          ))}
        </div>
      </Panel>
    </WorkspaceShell>
  );
}
